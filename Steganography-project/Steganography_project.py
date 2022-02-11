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
        showEncodedMessage = 1

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
                        if(counter == len(binaryMessageString) and showEncodedMessage != 0):
                            colorName = "black"
                            if(color == 0):
                                colorName = "red"
                            if(color == 1):
                                colorName = "green"
                            if(color == 2):
                                colorName = "blue"
                            print("Message \""+ message +"\" encoded (last encoded pixel color: "+colorName +")")
                            print("")
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
        filterOutWeirdSigns = 1 # filters characters that do not belong between 32 and 127 ASCII values (inclusive)

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
                        hiddenBinaryMessage += str(num)
                    if(color == 1):
                        #print("Pixel(G)", counter-imageSize, "(", self.image[i][j],")")                                                
                        num = (self.image[i][j])[1]%2
                        num = num.item()
                        hiddenBinaryMessage += str(num)
                    if(color == 2):      
                        #print("Pixel(B)", counter-imageSize*2, "(", self.image[i][j],")")                                                
                        num = (self.image[i][j])[2]%2
                        num = num.item()
                        hiddenBinaryMessage += str(num)

        #print("")                
        #print("Decoded message (binary): ", hiddenBinaryMessage)
        #print("")  

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
        
        if(filterOutWeirdSigns != 0):
            old = hiddenMessage
            hiddenMessage = ""
            for c in old:
                if(ord(c)<32 or ord(c)>127):
                    break;
                else:
                    hiddenMessage = hiddenMessage + c

        print("Decoded message (characters): ")
        print(hiddenMessage)
        print("")  

class Steganalyzer:

    image = np.zeros([100,100,3],dtype=np.uint8)
    image.fill(0)
    imageLink = ""

    unmodifiedImage = np.zeros([100,100,3],dtype=np.uint8)
    unmodifiedImage.fill(0)
    unmodifiedImageLink = ""

    def LoadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)
        self.imageLink=link

        # Used to load unmodified image, one used to compare with modified
    def loadUnmodifiedImage(self, link):
        self.unmodifiedImage = cv.imread(link, cv.IMREAD_COLOR)
        self.unmodifiedImageLink=link

    def getHistogram(self, image, color_channel_id):
        plt.xlim([0, 256])
        histogram, bin_edges = np.histogram(image[:, :, color_channel_id], bins=256, range=(0, 256))
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
        return histogramPairValues

    def getPairValuesAverages(self, pairValues):
        PairValuesAverages = list()
        for pair in pairValues:
            avg = 0
            if((pair[0]+pair[1]) != 0):
                avg=(pair[0]+pair[1])/2
            PairValuesAverages.append(avg)
        return PairValuesAverages

    def getPairValuesAverages2(self, values):
        PairValuesAverages = list()
        i = 0
        avg = 0
        for i in range(len(values)-1):
            avg = 0
            if((values[i]+values[i+1]) != 0):
                avg=(values[i]+values[i+1])/2
            PairValuesAverages.append(avg)
        print("PairValuesAverages len: ", len(PairValuesAverages))
        return PairValuesAverages

    def getPairValuesAverages3(self, values):
        PairValuesAverages = list()
        i = 0
        avg = 0
        for i in range(len(values)-1):
            if(i%2==0):
                avg = 0
                if((values[i]+values[i+1]) != 0):
                    avg=(values[i]+values[i+1])/2
                PairValuesAverages.append(avg)
        print("PairValuesAverages len: ", len(PairValuesAverages))
        return PairValuesAverages
        
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

    def getOddIndexElements(self, elements):
        oddIndexElements = []
        i=0
        for i in range(len(elements)):
            if(i%2==1):
                oddIndexElements.append(elements[i])
        return oddIndexElements


        # Prints out comparison of values needed for chi test
    def printComparisionTable(self, OddIndexAverages, e, OddIndexAverages2, e2):
        blankimage = np.zeros([100,100,3],dtype=np.uint8)
        blankimage.fill(0) # or img[:] = 255
        if(self.unmodifiedImageLink != ""):
            print("________________________________________")
            print("original image is loaded for comparision")
            print("____|edited image   |   original image")
            for i in range(len(e)):
                print("["+ str(i) +"]: Odd: "+ str(OddIndexAverages[i]) +", e: "+  str(e[i]) + "   |   Odd: "+ str(OddIndexAverages2[i]) +", e: "+  str(e2[i]) + " ")
        else:
            for i in range(len(e)):
                print("["+ str(i) +"]: Odd: "+ str(OddIndexAverages[i]) +", e: "+  str(e[i]))

    def AnalyzeImage(self, values):
        print("Commencing single image analysis...")  
        histogram_R, bin_edges = self.getHistogram(values, 0)
        histogramPairValues = self.getHistogramPairValues(histogram_R)
        #e = self.getPairValuesAverages(histogramPairValues)
        e = self.getPairValuesAverages3(histogram_R)
        OddIndexes = self.getOddIndexElements(histogram_R)

        return histogram_R, bin_edges, histogramPairValues, e, OddIndexes
    
    def ChiSquareTest(self, observed, expected):
        #try:
        chi, p = sp.stats.chisquare(observed, f_exp=expected)            
        print("ChiSquare test: p = ", p)
        #except:
        #    print("Chisquare ValueError...")
        ## ValueError: For each axis slice, the sum of the observed frequencies must agree
        ## with the sum of the expected frequencies to a relative tolerance of 1e-08, but the percent differences are:

        #pair of values analysis
    def Analyze(self):
        print("Commencing analysis...")  
        histogram_R, bin_edges, histogramPairValues, e, OddIndexes = self.AnalyzeImage(self.image)

        #histogram_R, bin_edges = self.getHistogram(self.image, 0)
        #histogramPairValues = self.getHistogramPairValues(histogram_R)
        ##e = self.getPairValuesAverages(histogramPairValues)
        #e = self.getPairValuesAverages3(histogram_R)
        #OddIndexes = self.getOddIndexElements(histogram_R)

        print("- histogram_R -----------")
        print(histogram_R[:])
        print("- histogramPairValues -----------")
        print(histogramPairValues[:])
        print("- e -----------")
        print(e[:])
        print("- OddIndexes -----------")
        print(OddIndexes[:])
        print("-----------")

        self.ChiSquareTest(e, OddIndexes)

        #print("len OddIndexAverages: ", len(OddIndexAverages))
        #print(OddIndexAverages)
        #print("len e: ", len(e))
        #print(e)
        
        #histogram_R_unmodified, bin_edges_unmodified = self.getHistogram(self.unmodifiedImage, 0)
        #histogramPairValues_unmodified = self.getHistogramPairValues(histogram_R_unmodified)
        #e_unmodified = self.getPairValuesAverages(histogramPairValues_unmodified)
        #OddIndexAverages_unmodified = self.getOddPairElements(histogramPairValues_unmodified)



        #self.printComparisionTable(OddIndexAverages, e, OddIndexAverages_unmodified, e_unmodified)

        observed=np.array(e[:])
        expected=np.array(OddIndexes[:])
                
        print("- histogram_R -----------")
        print(histogram_R)
        print("- histogramPairValues -----------")
        print(histogramPairValues)
        print("- e -----------")
        print(e[:])
        print("- OddIndexAverages -----------")
        print(OddIndexes[:])
        print("-----------")


        #self.compareHistograms(histogram_R, histogram_R_unmodified, bin_edges, bin_edges_unmodified, "red", "black")
        plt.show()
        
 


messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc quis ante sit amet erat porttitor luctus. Sed justo nulla, interdum ac elit eget, viverra elementum est. Quisque porta metus nisi, nec malesuada dolor suscipit id. Ut vehicula congue nulla, vitae mattis tortor sollicitudin pellentesque."
#messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non lobortis neque, sed varius lacus. Etiam dapibus iaculis efficitur. Duis lectus nisl, tincidunt nec placerat sed, porta ac elit. Maecenas leo lacus, congue ac quam mattis, luctus vestibulum sem. Quisque eget nisi eu mi tempus dictum. Aenean eu suscipit felis, vitae porttitor mauris. Maecenas velit nunc, vulputate nec tristique vel, consequat in ipsum. Ut sed metus eget tellus bibendum laoreet quis ut sem. Vestibulum quis vestibulum sem. Curabitur condimentum augue vel eros sagittis ultricies. Vivamus ut est commodo, lacinia lorem non, mattis nunc. Curabitur mattis tortor lobortis vehicula ultricies. Aenean tortor lorem, venenatis nec sollicitudin non, scelerisque ac erat. Mauris iaculis eleifend neque. Ut vitae laoreet eros. Donec fringilla enim eu arcu aliquet fermentum. Donec malesuada sollicitudin nisl non faucibus. Sed eleifend vulputate vehicula. Ut et lorem tempor, porta arcu vitae, egestas nunc. Integer tempus vitae nulla vitae blandit."
#messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non lobortis neque, sed varius lacus. Etiam dapibus iaculis efficitur. Duis lectus nisl, tincidunt nec placerat sed, porta ac elit. Maecenas leo lacus, congue ac quam mattis, luctus vestibulum sem. Quisque eget nisi eu mi tempus dictum. Aenean eu suscipit felis, vitae porttitor mauris. Maecenas velit nunc, vulputate nec tristique vel, consequat in ipsum. Ut sed metus eget tellus bibendum laoreet quis ut sem. Vestibulum quis vestibulum sem. Curabitur condimentum augue vel eros sagittis ultricies. Vivamus ut est commodo, lacinia lorem non, mattis nunc. Curabitur mattis tortor lobortis vehicula ultricies. Aenean tortor lorem, venenatis nec sollicitudin non, scelerisque ac erat. Mauris iaculis eleifend neque. Ut vitae laoreet eros. Donec fringilla enim eu arcu aliquet fermentum. Donec malesuada sollicitudin nisl non faucibus. Sed eleifend vulputate vehicula. Ut et lorem tempor, porta arcu vitae, egestas nunc. Integer tempus vitae nulla vitae blandit. Nam in dolor ac metus sodales tincidunt. Integer venenatis urna ligula, et mattis mauris aliquam quis. Donec sit amet nulla vel orci faucibus luctus. Pellentesque commodo nisi dolor, ut egestas elit venenatis ac. Aenean in felis viverra, interdum magna id, consectetur magna. Nullam mollis tincidunt nisi, sed blandit dui bibendum vitae. In suscipit, nisi sed gravida malesuada, nibh libero maximus dolor, non eleifend nisl elit a nisi. Praesent ac luctus tellus. Quisque imperdiet purus eget maximus feugiat. Curabitur sollicitudin rhoncus finibus. Aliquam vehicula tincidunt enim, in rutrum ipsum cursus ac. Nulla gravida dui eget augue fringilla, mollis gravida metus euismod."
#messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non lobortis neque, sed varius lacus. Etiam dapibus iaculis efficitur. Duis lectus nisl, tincidunt nec placerat sed, porta ac elit. Maecenas leo lacus, congue ac quam mattis, luctus vestibulum sem. Quisque eget nisi eu mi tempus dictum. Aenean eu suscipit felis, vitae porttitor mauris. Maecenas velit nunc, vulputate nec tristique vel, consequat in ipsum. Ut sed metus eget tellus bibendum laoreet quis ut sem. Vestibulum quis vestibulum sem. Curabitur condimentum augue vel eros sagittis ultricies. Vivamus ut est commodo, lacinia lorem non, mattis nunc. Curabitur mattis tortor lobortis vehicula ultricies. Aenean tortor lorem, venenatis nec sollicitudin non, scelerisque ac erat. Mauris iaculis eleifend neque. Ut vitae laoreet eros. Donec fringilla enim eu arcu aliquet fermentum. Donec malesuada sollicitudin nisl non faucibus. Sed eleifend vulputate vehicula. Ut et lorem tempor, porta arcu vitae, egestas nunc. Integer tempus vitae nulla vitae blandit. Nam in dolor ac metus sodales tincidunt. Integer venenatis urna ligula, et mattis mauris aliquam quis. Donec sit amet nulla vel orci faucibus luctus. Pellentesque commodo nisi dolor, ut egestas elit venenatis ac. Aenean in felis viverra, interdum magna id, consectetur magna. Nullam mollis tincidunt nisi, sed blandit dui bibendum vitae. In suscipit, nisi sed gravida malesuada, nibh libero maximus dolor, non eleifend nisl elit a nisi. Praesent ac luctus tellus. Quisque imperdiet purus eget maximus feugiat. Curabitur sollicitudin rhoncus finibus. Aliquam vehicula tincidunt enim, in rutrum ipsum cursus ac. Nulla gravida dui eget augue fringilla, mollis gravida metus euismod. Donec vitae sapien non arcu viverra euismod. Nam dapibus ultricies leo sed mollis. Donec cursus risus arcu, sit amet faucibus leo pulvinar vitae. Nam commodo volutpat porttitor. Ut convallis hendrerit sapien, in laoreet justo rutrum sed. Duis a ligula et diam consectetur lacinia sagittis quis ipsum. Integer accumsan dolor urna, sed suscipit risus pharetra sed. Nullam cursus libero sed elit aliquet aliquet. Praesent non elementum ligula. Aenean in libero at odio tristique vulputate nec sed augue. Ut tellus enim, consequat eget hendrerit non, sagittis vel turpis. Aliquam ullamcorper rhoncus fermentum. In commodo sodales nibh et rhoncus. Maecenas at diam vestibulum arcu molestie rhoncus quis sed nunc. Aliquam blandit faucibus erat, et pulvinar neque suscipit at. Pellentesque erat elit, pellentesque id pharetra sed, laoreet non risus. Donec auctor euismod fringilla. Curabitur dapibus elit sollicitudin eros finibus feugiat et vehicula lectus. Nunc feugiat risus et tristique bibendum. Etiam porttitor, massa sed laoreet porttitor, nibh arcu vehicula felis, faucibus semper dolor augue non felis. Sed et diam fringilla, viverra ante vel, interdum tortor. Cras semper ipsum non purus tincidunt accumsan. Integer dui magna, feugiat at rutrum a, rhoncus sed nunc. In hac habitasse platea dictumst."

encoder = SteganographyEncoder()
encoder.loadImage("images/arbismall.png")
encoder.encodeMessage(messageToEncode)
encoder.saveImage("images/saved.png")

decoder = SteganographyDecoder()
decoder.loadImage("images/saved.png")
decoder.printMessageIfAny()

steganalyzer = Steganalyzer()

steganalyzer.LoadImage("images/saved.png")
steganalyzer.loadUnmodifiedImage("images/forest_small.png")
steganalyzer.Analyze()


#plt.figure()
#plt.imshow(cv.cvtColor(encoder.image, cv.COLOR_BGR2RGB))
#plt.figure()
#plt.imshow(cv.cvtColor(encoder.encodedImage, cv.COLOR_BGR2RGB))

