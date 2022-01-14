import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2 as cv

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

        #TODO
        #old = binaryMessageString
        #binaryMessageString=""
        #counter = -1
        #for c in old:
        #    counter+=1
        #    if(counter==0):
        #        binaryMessageString+="0"
        #        binaryMessageString+=c
        #    elif(counter==6):
        #        binaryMessageString+=c
        #        counter=-1
        #    else:
        #        binaryMessageString+=c

        #print("(nakon) Binarni niz: ", binaryMessageString)
        #print("(nakon) Duljina binarnog niza: ", len(binaryMessageString))
        
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
        #self.image = mpimg.imread(link)
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

        #for n in hiddenBinaryMessage:
        #    counter += 1
        #    if(counter == 7):
        #        binaryChar = binaryChar + n 

        #        #print(binaryChar + " " + str(int(binaryChar, 2)) + " " + chr(int(binaryChar, 2))) #TODO

        #        hiddenMessage = hiddenMessage + chr(int(binaryChar, 2))
        #        binaryChar=""
        #        counter = -1
        #    else:
        #        binaryChar = binaryChar + n    

        print("")  
        print("Decoded message (characters): ")
        print(hiddenMessage)
        print("")  






messageToEncode = "Pozdrav svijete!"

encoder = SteganographyEncoder()
encoder.loadImage("images/arbismall.png")
encoder.encodeMessage(messageToEncode)
encoder.saveImage("images/saved.png")

decoder = SteganographyDecoder()
decoder.loadImage("images/saved.png")
decoder.printMessageIfAny()

plt.imshow(cv.cvtColor(encoder.image, cv.COLOR_BGR2RGB))
plt.figure()
plt.imshow(cv.cvtColor(encoder.encodedImage, cv.COLOR_BGR2RGB))
plt.show()