import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2 as cv
import scipy as sp
import math
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
                            print("\n~~~~~~~~~~~~~~~~~~~~~~~~ Steganography Encoder ~~~~~~~~~~~~~~~~~~~~~~~~")
                            print("Message \""+ message +"\" encoded (last encoded pixel color: "+colorName +")")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 
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
        if(counter < len(binaryMessageString)):
            print("Warning: Message is not fully encoded.")
        
class SteganographyDecoder:

    image = np.zeros([100,100,3],dtype=np.uint8)
    image.fill(0) # or img[:] = 255

    def loadImage(self, link):
        self.image = cv.imread(link, cv.IMREAD_COLOR)

        # argument 1: if true: filters characters that do not belong between 32 and 127 ASCII values (inclusive)
    def decode(self, messageFilter):    

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
        
        if(messageFilter != 0):
            old = hiddenMessage
            hiddenMessage = ""
            for c in old:
                if(ord(c)<32 or ord(c)>127):
                    break;
                else:
                    hiddenMessage = hiddenMessage + c
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~ Steganography Decoder ~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Decoded message: ")
        print(hiddenMessage)  
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

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
  
        # ? Prints out comparison of values needed for chi test
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

    def getPairValuesAverages(self, values):
        PairValuesAverages = list()
        i = 0
        avg = 0
        for i in range(len(values)-1):
            if(i%2==0):
                avg=(values[i]+values[i+1])/2
                PairValuesAverages.append(avg)
        return PairValuesAverages

    def getOddIndexElements(self, elements):
        oddIndexElements = []
        i=0
        for i in range(len(elements)):
            if(i%2==1):
                oddIndexElements.append(elements[i])
        return oddIndexElements

    def GetImageChannelFeatures(self, values, color):
        c=0
        if(color == 0 or color == 1 or color == 2):
            c=color
        else:
            print("GetImageChannelFeatures warning: wrong color channel input, channel 0 taken")

        #print("\n\nGetImageChannelFeatures...color: ", color, ", ", c)  
        histogramData, bin_edges = self.getHistogram(values, c)
        histogramPairValues = self.getHistogramPairValues(histogramData)
        e = self.getPairValuesAverages(histogramData)
        OddIndexes = self.getOddIndexElements(histogramData)

        return histogramData, bin_edges, histogramPairValues, e, OddIndexes
    
    def ChiSquareTest(self, observed, expected):

        ## ↓ removing elements from arrays where 'expected' has zero ↓

        observed2 = []
        expected2 = []

        for x in range(len(expected)-1):
            observed2.append(observed[x])
            expected2.append(expected[x])

        for x in reversed(range(len(expected)-1)):
            if(expected[x] == 0):
                observed2.pop(x)
                expected2.pop(x)

        #print("Observed2 sum: ", np.sum(observed2))
        #print("Expected2 sum: ", np.sum(expected2))

        ## ↑ removing elements from arrays where 'expected' has zero ↑
        ## ↓ equalizing sums of expected and observed ↓

        exp_sum = sum(expected2)
        obs_sum = sum(observed2)

        exp2 = (expected2/exp_sum)*obs_sum
        #print("!! ", sum(exp2), "!!", sum(observed2))

        ## ↑ equalizing sums of expected and observed ↑

        chi, p = sp.stats.chisquare(observed2, exp2, 0)            
        return p

    def PrintHistogramValues(self, histogram, e, OddIndexes):
        print("\n--------------------------")
        print("\n- histogram -----------")
        print(histogram[:])
        print("\n- e -----------")
        print(e[:])
        print("\n- OddIndexes -----------")
        print(OddIndexes[:])
        print("--------------------------")
 
    def Analyze(self, nRowsToCheck):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Steganalyzer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if(nRowsToCheck>self.image.shape[1]):
            nRowsToCheck = self.image.shape[1]

        print("nRowsToCheck: ", nRowsToCheck, "[", nRowsToCheck/self.image.shape[1]*100, "%]")

        image2 = np.zeros([100,100,3],dtype=np.uint8)
        image2 = self.image[0:nRowsToCheck,:,:]

        #plt.figure()
        #plt.imshow(cv.cvtColor(image2, cv.COLOR_BGR2RGB))
        #plt.show()

        histogram_R, bin_edges, histogramPairValues, e0, OddIndexes0 = self.GetImageChannelFeatures(image2, 0)
        #self.PrintHistogramValues(histogram_R, e0, OddIndexes0)
        result0 = self.ChiSquareTest(OddIndexes0, e0)

        histogram_G, bin_edges, histogramPairValues, e1, OddIndexes1 = self.GetImageChannelFeatures(image2, 1)
        #self.PrintHistogramValues(histogram_G, e1, OddIndexes1)
        result1 = self.ChiSquareTest(OddIndexes1, e1)

        histogram_B, bin_edges, histogramPairValues, e2, OddIndexes2 = self.GetImageChannelFeatures(image2, 2)
        #self.PrintHistogramValues(histogram_B, e2, OddIndexes2)
        result2 = self.ChiSquareTest(OddIndexes2, e2)

        print("Probability of data in red channel: ", result0)
        print("Probability of data in green channel: ", result1)
        print("Probability of data in blue channel: ", result2)        
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 

#messageToEncode = ""
#messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
#messageToEncode3 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc quis ante sit amet erat porttitor luctus. Sed justo nulla, interdum ac elit eget, viverra elementum est. Quisque porta metus nisi, nec malesuada dolor suscipit id. Ut vehicula congue nulla, vitae mattis tortor sollicitudin pellentesque."
#messageToEncode2 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non lobortis neque, sed varius lacus. Etiam dapibus iaculis efficitur. Duis lectus nisl, tincidunt nec placerat sed, porta ac elit. Maecenas leo lacus, congue ac quam mattis, luctus vestibulum sem. Quisque eget nisi eu mi tempus dictum. Aenean eu suscipit felis, vitae porttitor mauris. Maecenas velit nunc, vulputate nec tristique vel, consequat in ipsum. Ut sed metus eget tellus bibendum laoreet quis ut sem. Vestibulum quis vestibulum sem. Curabitur condimentum augue vel eros sagittis ultricies. Vivamus ut est commodo, lacinia lorem non, mattis nunc. Curabitur mattis tortor lobortis vehicula ultricies. Aenean tortor lorem, venenatis nec sollicitudin non, scelerisque ac erat. Mauris iaculis eleifend neque. Ut vitae laoreet eros. Donec fringilla enim eu arcu aliquet fermentum. Donec malesuada sollicitudin nisl non faucibus. Sed eleifend vulputate vehicula. Ut et lorem tempor, porta arcu vitae, egestas nunc. Integer tempus vitae nulla vitae blandit."
#messageToEncode2 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non lobortis neque, sed varius lacus. Etiam dapibus iaculis efficitur. Duis lectus nisl, tincidunt nec placerat sed, porta ac elit. Maecenas leo lacus, congue ac quam mattis, luctus vestibulum sem. Quisque eget nisi eu mi tempus dictum. Aenean eu suscipit felis, vitae porttitor mauris. Maecenas velit nunc, vulputate nec tristique vel, consequat in ipsum. Ut sed metus eget tellus bibendum laoreet quis ut sem. Vestibulum quis vestibulum sem. Curabitur condimentum augue vel eros sagittis ultricies. Vivamus ut est commodo, lacinia lorem non, mattis nunc. Curabitur mattis tortor lobortis vehicula ultricies. Aenean tortor lorem, venenatis nec sollicitudin non, scelerisque ac erat. Mauris iaculis eleifend neque. Ut vitae laoreet eros. Donec fringilla enim eu arcu aliquet fermentum. Donec malesuada sollicitudin nisl non faucibus. Sed eleifend vulputate vehicula. Ut et lorem tempor, porta arcu vitae, egestas nunc. Integer tempus vitae nulla vitae blandit. Nam in dolor ac metus sodales tincidunt. Integer venenatis urna ligula, et mattis mauris aliquam quis. Donec sit amet nulla vel orci faucibus luctus. Pellentesque commodo nisi dolor, ut egestas elit venenatis ac. Aenean in felis viverra, interdum magna id, consectetur magna. Nullam mollis tincidunt nisi, sed blandit dui bibendum vitae. In suscipit, nisi sed gravida malesuada, nibh libero maximus dolor, non eleifend nisl elit a nisi. Praesent ac luctus tellus. Quisque imperdiet purus eget maximus feugiat. Curabitur sollicitudin rhoncus finibus. Aliquam vehicula tincidunt enim, in rutrum ipsum cursus ac. Nulla gravida dui eget augue fringilla, mollis gravida metus euismod."
messageToEncode = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non lobortis neque, sed varius lacus. Etiam dapibus iaculis efficitur. Duis lectus nisl, tincidunt nec placerat sed, porta ac elit. Maecenas leo lacus, congue ac quam mattis, luctus vestibulum sem. Quisque eget nisi eu mi tempus dictum. Aenean eu suscipit felis, vitae porttitor mauris. Maecenas velit nunc, vulputate nec tristique vel, consequat in ipsum. Ut sed metus eget tellus bibendum laoreet quis ut sem. Vestibulum quis vestibulum sem. Curabitur condimentum augue vel eros sagittis ultricies. Vivamus ut est commodo, lacinia lorem non, mattis nunc. Curabitur mattis tortor lobortis vehicula ultricies. Aenean tortor lorem, venenatis nec sollicitudin non, scelerisque ac erat. Mauris iaculis eleifend neque. Ut vitae laoreet eros. Donec fringilla enim eu arcu aliquet fermentum. Donec malesuada sollicitudin nisl non faucibus. Sed eleifend vulputate vehicula. Ut et lorem tempor, porta arcu vitae, egestas nunc. Integer tempus vitae nulla vitae blandit. Nam in dolor ac metus sodales tincidunt. Integer venenatis urna ligula, et mattis mauris aliquam quis. Donec sit amet nulla vel orci faucibus luctus. Pellentesque commodo nisi dolor, ut egestas elit venenatis ac. Aenean in felis viverra, interdum magna id, consectetur magna. Nullam mollis tincidunt nisi, sed blandit dui bibendum vitae. In suscipit, nisi sed gravida malesuada, nibh libero maximus dolor, non eleifend nisl elit a nisi. Praesent ac luctus tellus. Quisque imperdiet purus eget maximus feugiat. Curabitur sollicitudin rhoncus finibus. Aliquam vehicula tincidunt enim, in rutrum ipsum cursus ac. Nulla gravida dui eget augue fringilla, mollis gravida metus euismod. Donec vitae sapien non arcu viverra euismod. Nam dapibus ultricies leo sed mollis. Donec cursus risus arcu, sit amet faucibus leo pulvinar vitae. Nam commodo volutpat porttitor. Ut convallis hendrerit sapien, in laoreet justo rutrum sed. Duis a ligula et diam consectetur lacinia sagittis quis ipsum. Integer accumsan dolor urna, sed suscipit risus pharetra sed. Nullam cursus libero sed elit aliquet aliquet. Praesent non elementum ligula. Aenean in libero at odio tristique vulputate nec sed augue. Ut tellus enim, consequat eget hendrerit non, sagittis vel turpis. Aliquam ullamcorper rhoncus fermentum. In commodo sodales nibh et rhoncus. Maecenas at diam vestibulum arcu molestie rhoncus quis sed nunc. Aliquam blandit faucibus erat, et pulvinar neque suscipit at. Pellentesque erat elit, pellentesque id pharetra sed, laoreet non risus. Donec auctor euismod fringilla. Curabitur dapibus elit sollicitudin eros finibus feugiat et vehicula lectus. Nunc feugiat risus et tristique bibendum. Etiam porttitor, massa sed laoreet porttitor, nibh arcu vehicula felis, faucibus semper dolor augue non felis. Sed et diam fringilla, viverra ante vel, interdum tortor. Cras semper ipsum non purus tincidunt accumsan. Integer dui magna, feugiat at rutrum a, rhoncus sed nunc. In hac habitasse platea dictumst."
messageToEncode = messageToEncode + messageToEncode
messageToEncode = messageToEncode + messageToEncode #+ messageToEncode
messageToEncode = messageToEncode + messageToEncode
messageToEncode = messageToEncode + messageToEncode

encoder = SteganographyEncoder()
encoder.loadImage("images/lenna.png")
encoder.encodeMessage(messageToEncode)
encoder.saveImage("images/saved.png")

decoder = SteganographyDecoder()
decoder.loadImage("images/saved.png")
decoder.decode(1)

print("\n")
print("********************** Edited image steganalysis: **********************")
steganalyzer = Steganalyzer()
steganalyzer.LoadImage("images/saved.png")
steganalyzer.Analyze(100)

print("\n")
print("************************************************************************")
print("********************* Unedited image steganalysis: *********************")
steganalyzer.LoadImage("images/lenna.png")
steganalyzer.Analyze(100)

#plt.figure()
#plt.imshow(cv.cvtColor(encoder.image, cv.COLOR_BGR2RGB))
#plt.figure()
#plt.imshow(cv.cvtColor(encoder.encodedImage, cv.COLOR_BGR2RGB))

