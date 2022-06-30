def detectionPics ( extSignal , seuil ) :
    P0 , P1 , P2=extSignal [:3]
    i =1
    while i <len ( extSignal ) −2 and not(P0<= P1 and P1 >= P2):
        P0 , P1=P1 , P2
        P2=extSignal [i +2]
        i=i +1
    return i

def pulsationCardiaque (signal , Te , seuil) :
    pics = [ ]
    deb = 0
    nbPoints = int ( 3 / Te )
    while deb+nbPoints < len ( signal ):
        deb = deb+detectionPics ( signal [ deb : deb+nbPoints ] , seuil )
        pics . append ( deb )
        periode_moy = ( pics[−1]− pics [0]) *Te / ( len ( pics ) −1)
    return 60 / periode_moy