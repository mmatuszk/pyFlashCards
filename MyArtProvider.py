import  wx
import os.path

ART_FORMAT_TEXT_BOLD         = wx.NewId()
ART_FORMAT_TEXT_ITALIC       = wx.NewId()
ART_FORMAT_TEXT_UNDERLINE    = wx.NewId()

class TangoArtProvider(wx.ArtProvider):
    def __init__(self, runtimepath):
        wx.ArtProvider.__init__(self)
        self.runtimepath = runtimepath

    def CreateBitmap(self, artid, client, size):
        # You can do anything here you want, such as using the same
        # image for any size, any client, etc., or using specific
        # images for specific sizes, whatever...

        # See end of file for the image data

        bmp = wx.NullBitmap

        if artid == wx.ART_NEW:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/document-new.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/document-new.png')).ConvertToBitmap()

        elif artid == wx.ART_FILE_OPEN:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/document-open.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/document-open.png')).ConvertToBitmap()

        elif artid == wx.ART_FILE_SAVE:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/document-save.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/document-save.png')).ConvertToBitmap()

        elif artid == wx.ART_FILE_SAVE_AS:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/document-save-as.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/document-save-as.png')).ConvertToBitmap()

        elif artid == wx.ART_GO_FORWARD:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/go-next.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/go-next.png')).ConvertToBitmap()

        elif artid == wx.ART_GO_BACK:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/go-previous.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/go-previous.png')).ConvertToBitmap()

        elif artid == ART_FORMAT_TEXT_BOLD:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/format-text-bold.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/format-text-bold.png')).ConvertToBitmap()

        elif artid == ART_FORMAT_TEXT_ITALIC:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/format-text-italic.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/format-text-italic.png')).ConvertToBitmap()

        elif artid == ART_FORMAT_TEXT_UNDERLINE:
            if size.width >= 32:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/32x32/actions/format-text-underline.png')).ConvertToBitmap()
            else:
                bmp = wx.Image(os.path.join(self.runtimepath, 'icons/tango/16x16/actions/format-text-underline.png')).ConvertToBitmap()

        return bmp
