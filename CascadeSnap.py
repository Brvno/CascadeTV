import gtk.gdk
import time


BUFFER_SIZE = 30

while True:
	for i in range(0,BUFFER_SIZE):
		time.sleep(.1)
		w = gtk.gdk.get_default_root_window()

		sz = w.get_size()
		print "The size of the window is %d x %d" % sz
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
		pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])

		print bytes(pb)

		if (pb != None):
		    pb.save("buffer/"+str(i)+".png","png")
    	    # img = open("screenshot.png")
		    
		    print "Screenshot saved to screenshot.png."
		else:
		    print "Unable to get the screenshot."


# import pyscreenshot as ImageGrab

# # fullscreen
# im=ImageGrab.grab()
# im.show()

# # part of the screen
# im=ImageGrab.grab(bbox=(10,10,510,510)) # X1,Y1,X2,Y2
# im.show()
