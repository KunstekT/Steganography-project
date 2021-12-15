import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#   Razviti jednostavan algoritam za steganografiju, gdje korisnik može unijeti proizvoljnu tekstualnu poruku koja će se sakriti u slici. 
#   Također je potrebna metoda dekodiranja skrivene poruke iz slika. 

#   Zatim razviti jednostavan algoritam za detekciju stenografskih poruka, 
#   koji će prepoznati da je u nekoj slici skrivena poruka.

#   Prikazati i opisati algoritme na primjerima. 
#   Opisati trenutno stanje stenografskih metoda i koje su njihove primjene.

class SteganographyEncoder:
    image = np.zeros([100,100,3],dtype=np.uint8)
    image.fill(255) # or img[:] = 255

    def loadImage(self, link):
        self.image = mpimg.imread(link)

    def saveImage(self, link):
        mpimg.imsave(link, self.image)

    def messageToBinary(self, message):
        binaryMessage=[]
        characterList=[]
        for i in message:
            characterList.append(ord(i))
        for i in characterList:
            binaryMessage.append(int(bin(i)[2:]))
        return binaryMessage

    def encodeMessage(self, message):
        binaryMessage = self.messageToBinary(message)
        binaryMessageString = ""
        for i in range(len(binaryMessage)):
            binaryMessageString += str(binaryMessage[i])
        print(binaryMessageString)
        print(len(binaryMessageString))
        counter = -1
        for color in range(3):
            for i in range(np.size(self.image, 0)):
                for j in range(np.size(self.image, 1)):
                    counter+=1
                    if(counter >= len(binaryMessageString)):
                        if(counter == len(binaryMessageString)):
                            print("Message encoded")
                    else:
                        print("Byte", counter, "(", binaryMessageString[counter],")")
                        if(binaryMessageString[counter]=='1'):    # todo - does it work?
                            a = self.image[i,j,color].astype(int)
                            a = a | 1
                            self.image[i,j,color] = a
                            print(self.image[i,j,color])
                        else:
                            a = self.image[i,j,color].astype(int)
                            a = a & ~1
                            self.image[i,j,color] = a
                            print(self.image[i,j,color])
                print("ROW:", i)
            print("COLOR:", color)
        

#def decodeMessage()

encoder = SteganographyEncoder()
messageToEncode = "Pozdrav, svijete!"
encoder.loadImage("images/arbiter.png")
print(encoder.messageToBinary(messageToEncode))

plt.imshow(encoder.image)
color = [0,1,2,3,4,5]
encoder.encodeMessage(messageToEncode)
#encoder.saveImage("images/saved.png")

plt.figure()
plt.imshow(encoder.image)
plt.show()
