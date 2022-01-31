import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2 as cv
import scipy as sp
from scipy import stats



#   Razviti jednostavan algoritam za steganografiju, gdje korisnik može unijeti proizvoljnu tekstualnu poruku koja će se sakriti u slici. 
#   Također je potrebna metoda dekodiranja skrivene poruke iz slika. 

#   Zatim razviti jednostavan algoritam za detekciju stenografskih poruka, 
#   koji će prepoznati da je u nekoj slici skrivena poruka.

#   Prikazati i opisati algoritme na primjerima. 
#   Opisati trenutno stanje stenografskih metoda i koje su njihove primjene.

        
class SteganographyEncoder:
   
    image = np.zeros([100,100,3],dtype=np.uint8)
    image.fill(0) # or img[:] = 255    
    encodedImage = np.zeros([100,100,3],dtype=np.uint8)
    encodedImage.fill(0) # or img[:] = 255

    def loadImage(self, link):
        #self.image = mpimg.imread(link)
        self.image = cv.imread(link, cv.IMREAD_COLOR)
        self.encodedImage = cv.imread(link, cv.IMREAD_COLOR)

    def saveImage(self, link):     
        cv.imwrite(link, self.encodedImage)
       # mpimg.imsave(link, self.image) # maybe change

    def messageToBinary(self, message):
        stringList = list()
        characterList=[]
        for i in message:
            x=ord(i)
            characterList.append(x)
        for i in characterList:
            s = str(int(bin(i)[2:]))
            if(len(s)==7):
                s = "0" + s
            elif(len(s)==6):
                s = "00" + s
            elif(len(s)==5):
                s = "000" + s
            elif(len(s)==4):
                s = "0000" + s
            elif(len(s)==3):
                s = "00000" + s
            elif(len(s)==2):
                s = "000000" + s
            elif(len(s)==1):
                s = "0000000" + s
            else:
                s = "00000000"
            stringList.append(s)
        return stringList
        

    def printByte(self, a):
        print(format(a, '0{}b'.format(8)))

    def encodeMessage(self, message):
        binaryMessageStringList = self.messageToBinary(message)
        binaryMessageString=""
        for s in binaryMessageStringList:
            binaryMessageString+=s

        #print("Binarni niz: ", binaryMessageString)
        #print("Duljina binarnog niza: ", len(binaryMessageString))
        
        counter = -1
        for color in range(3):
            for i in range(np.size(self.encodedImage, 0)):
                for j in range(np.size(self.encodedImage, 1)):
                    counter+=1
                    if(counter >= len(binaryMessageString)):
                        if(counter == len(binaryMessageString)):
                            print("Message \""+ message +"\" encoded")
                    else:
                        #print("Byte", counter, "(", binaryMessageString[counter],")")
                        if(binaryMessageString[counter]=='1'):
                            a = self.encodedImage[i,j,color].astype(int)
                            #self.printByte(a)
                            a = a | 1
                            #self.printByte(a)
                            self.encodedImage[i,j,color] = a
                        else:
                            a = self.encodedImage[i,j,color].astype(int)
                            #self.printByte(a)
                            a = a & ~1
                            #self.printByte(a)
                            self.encodedImage[i,j,color] = a
            #    print("ROW:", i)
            #print("COLOR:", color)
        
class SteganographyDecoder:

    image = np.zeros([100,100,3],dtype=np.uint8)
    image.fill(0) # or img[:] = 255

    def loadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)

    def printMessageIfAny(self):     

        hiddenBinaryMessage = ""
        
        counter = -1
        xy = np.shape(self.image)
        imageSize=xy[0]*xy[1]
        for color in range(3):
            for i in range(np.size(self.image, 0)):
                for j in range(np.size(self.image, 1)):
                    counter+=1
                    if(color == 0):
                        #print("Pixel(R)", counter, "(", self.image[i][j],")")
                        num = (self.image[i][j])[0]%2
                        num = num.item()
                        #print(num)
                        hiddenBinaryMessage += str(num)
                    if(color == 1):
                        #print("Pixel(G)", counter-imageSize, "(", self.image[i][j],")")                                                
                        num = (self.image[i][j])[1]%2
                        num = num.item()
                        #print(num)
                        hiddenBinaryMessage += str(num)
                    if(color == 2):      
                        #print("Pixel(B)", counter-imageSize*2, "(", self.image[i][j],")")                                                
                        num = (self.image[i][j])[2]%2
                        num = num.item()
                        #print(num)
                        hiddenBinaryMessage += str(num)
        print("")                
        print("Decoded message (binary): ", hiddenBinaryMessage)
        print("")  

        hiddenMessage = ""
        binaryChar = ""
        counter = -1
        for n in hiddenBinaryMessage:
            counter += 1
            if(counter == 7):
                binaryChar = binaryChar + n 

                #print(binaryChar + " " + str(int(binaryChar, 2)) + " " + chr(int(binaryChar, 2)))

                if(int(binaryChar, 2)>31):
                    hiddenMessage += chr(int(binaryChar, 2))

                binaryChar=""
                counter = -1
            else:
                binaryChar = binaryChar + n     

        print("")  
        print("Decoded message (characters): ")
        print(hiddenMessage)
        print("")  

class Steganalyzer:

    image = np.zeros([100,100,3],dtype=np.uint8)
    image.fill(0) # or img[:] = 255
    imageLink = ""

    unmodifiedImage = np.zeros([100,100,3],dtype=np.uint8)
    unmodifiedImage.fill(0) # or img[:] = 255
    unmodifiedImageLink = ""

    def LoadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)
        self.imageLink=link

        #Used to load unmodified image, to compare with modified
    def loadUnmodifiedImage(self, link):
        self.unmodifiedImage = cv.imread(link, cv.IMREAD_COLOR)
        self.unmodifiedImageLink=link

    def getHistogram(self, image, color_channel_id):

        color="black"
        plt.xlim([0, 256])

        histogram, bin_edges = np.histogram(
        image[:, :, color_channel_id], bins=256, range=(0, 256)
        )
        if(color_channel_id==0):
            color="red"
        elif(color_channel_id==1):
            color="green"
        elif(color_channel_id==2):
            color="blue"
        else:
            color="black"

        return histogram, bin_edges


    def showHistogram(self, histogram, bin_edges, color):
        #plt.figure()
        plt.plot(bin_edges[0:-1], histogram, color)
        #print(histogram)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram of \"" + self.imageLink + "\", color channel: " + color)


    def compareHistograms(self, histogram1, histogram2, bin_edges1, bin_edges2, color1, color2):
        #plt.figure()
        plt.plot(bin_edges1[0:-1], histogram1, color1)
        plt.plot(bin_edges2[0:-1], histogram2, color2)
        #print(histogram)
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
        plt.title("Histogram comparision")
      

    def getHistogramPairValues(self, histogram):
        pairvalue=list()
        histogramPairValues = list()
        i=1
        for i in range(256):
            pairvalue.clear()
            if(i%2==1):
                pairvalue.append(histogram[i-1])
                pairvalue.append(histogram[i])
                vectorpairvalue = np.array(pairvalue)
                histogramPairValues.append(vectorpairvalue)

        print("histogramPairValues len: ", len(histogramPairValues))
        #print("histogramPairValues")
        #print(histogramPairValues[:])
        return histogramPairValues


    def getPairValuesAverages(self, pairValues):
        PairValuesAverages = list()
        for pair in pairValues:
            avg = 0
            if((pair[0]+pair[1]) != 0):
                avg=(pair[0]+pair[1])/2
            PairValuesAverages.append(avg)
        print("PairValuesAverages len: ", len(PairValuesAverages))
        return PairValuesAverages


    #def getOddIndexElements(self, elements):
    #    OddIndexElements = []
    #    i=0
    #    for i in range(len(elements)):
    #        if(i%2==1):
    #            OddIndexElements.append(elements[i])
    #    return OddIndexElements

        
        #???
    def getOddPairElements(self, elements):
        OddPairElements = []
        i=0
        #print("elements")
        #print(elements)
        pair = []
        x=0
        for i in range(len(elements)):
            pair = elements[i]
            #print("getOddPairElements Pair: ", pair)
            x = pair[1]
            #print("getOddPairElements x: ", x)
            OddPairElements.append(x)
        return OddPairElements


        # divides the height of an image by imageShrinkFactor
    def shrinkImage(self, image, imageShrinkFactor):
        img = image
        if(imageShrinkFactor < 1):
            imageShrinkFactor = 1
        #img_shrinked = cv.resize(img, (0, 0), fx=1/imageShrinkFactor, fy=1/imageShrinkFactor)
        #cv.resize(img, img.size/imageShrinkFactor)
        y=0
        x=0

        h=int(img.shape[0])/int(imageShrinkFactor)
        w=img.shape[1]
        print("Height: ", h)
        print("Width: ", w)

        crop_img = img[y:y+int(h), x:x+int(w)]
        #cv.imshow("cropped", crop_img)
        #cv.waitKey(0)
        return crop_img


        # Prints out comparison of values needed for chi test
    def printComparisionTable(self, OddIndexAverages, e, OddIndexAverages2, e2):
        blankimage = np.zeros([100,100,3],dtype=np.uint8)
        blankimage.fill(0) # or img[:] = 255
        if(self.unmodifiedImageLink != ""):
            print("________________________________________")
            print("original image is loaded for comparision")
            print("____|edited image; original image")
            for i in range(len(e)):
                print("["+ str(i) +"]: Odd: "+ str(OddIndexAverages[i]) +", e: "+  str(e[i]) + " {Odd: "+ str(OddIndexAverages2[i]) +", e: "+  str(e2[i]) + "}")
        else:
            for i in range(len(e)):
                print("["+ str(i) +"]: Odd: "+ str(OddIndexAverages[i]) +", e: "+  str(e[i]))


        #pair of values analysis
    def Analyze(self):
        print("Commencing analysis...")  

        #im = self.shrinkImage(self.image, 4)
        #histogram_R_shrinked, bin_edges_shrinked = self.getHistogram(im, 0)
        
        #plt.imshow(cv.cvtColor(im, cv.COLOR_BGR2RGB))
        #plt.figure()

        #self.showHistogram(histogram_R_shrinked, bin_edges_shrinked, "red")
        #histogramPairValues_shrinked = self.getHistogramPairValues(histogram_R_shrinked)
        #e_shrinked = self.getPairValuesAverages(histogramPairValues_shrinked)
        #OddIndexAverages_shrinked = self.getOddPairElements(histogramPairValues_shrinked)
        #plt.figure()

        histogram_R, bin_edges = self.getHistogram(self.image, 0)
        #self.showHistogram(histogram_R, bin_edges, "red")

        histogramPairValues = self.getHistogramPairValues(histogram_R)
        e = self.getPairValuesAverages(histogramPairValues)
        OddIndexAverages = self.getOddPairElements(histogramPairValues)



        #print("len OddIndexAverages: ", len(OddIndexAverages))
        #print(OddIndexAverages)
        #print("len e: ", len(e))
        #print(e)

        histogram_R_unmodified, bin_edges_unmodified = self.getHistogram(self.unmodifiedImage, 0)

        histogramPairValues_unmodified = self.getHistogramPairValues(histogram_R_unmodified)

        OddIndexAverages_unmodified= self.getOddPairElements(histogramPairValues_unmodified)
        e_unmodified=self.getPairValuesAverages(histogramPairValues_unmodified)

        self.compareHistograms(histogram_R, histogram_R_unmodified, bin_edges, bin_edges_unmodified, "red", "black")
        plt.show()
        
        self.printComparisionTable(OddIndexAverages, e, OddIndexAverages_unmodified, e_unmodified)


        chi, p = sp.stats.chisquare([16, 18, 16, 14, 12, 12], f_exp=[16, 16, 16, 16, 16, 8])
        print("Vjerojatnost IDK: ", p)

        observed=np.array(OddIndexAverages[0:8])
        expected=np.array(e[0:8])

        print("Observed: ")
        print(observed)
        print("Expected: ")
        print(expected)

        chi, p = sp.stats.chisquare(observed, expected, 0)
        print("Vjerojatnost da su OddIndexAverages i e u istoj distribuciji: p = ", p)
        #ValueError: For each axis slice, the sum of the observed frequencies must agree
        #with the sum of the expected frequencies to a relative tolerance of 1e-08, but the percent differences are:



        
 


messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc quis ante sit amet erat porttitor luctus. Sed justo nulla, interdum ac elit eget, viverra elementum est. Quisque porta metus nisi, nec malesuada dolor suscipit id. Ut vehicula congue nulla, vitae mattis tortor sollicitudin pellentesque."


encoder = SteganographyEncoder()
encoder.loadImage("images/forest.jpeg")
encoder.encodeMessage(messageToEncode)
encoder.saveImage("images/saved.png")

decoder = SteganographyDecoder()
decoder.loadImage("images/saved.png")
decoder.printMessageIfAny()

steganalyzer = Steganalyzer()
steganalyzer.LoadImage("images/saved.png")
steganalyzer.loadUnmodifiedImage("images/forest.jpeg")
steganalyzer.Analyze()



#plt.figure()
#plt.imshow(cv.cvtColor(encoder.image, cv.COLOR_BGR2RGB))
#plt.figure()
#plt.imshow(cv.cvtColor(encoder.encodedImage, cv.COLOR_BGR2RGB))
