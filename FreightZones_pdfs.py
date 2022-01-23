from qgis.PyQt import QtGui
import math
import os

#Below is a function that checks the spelling of a word against all words in a list of words.
#If that word is different to all the words in a list but at least 80 percent of the letters of
#that word are in any word in the list, the words in the list will be added to an array. The
#function returns that array. This function was created for the purpose of checking for spelling
#mistakes
#The function takes in string 'wordtocheck' and an array of strings 'WordList' and returns the array
#'suggestedwords'
def checkspellings(wordtocheck, WordList):
    numwordsinlist = len(WordList)
    wordlength = len(wordtocheck)
    suggestedwords = []
    
    for k in range(numallwords):
        thiswordfromlist = WordList[k]
        thiswordlength = len(thiswordfromlist)
        count = 0
        for i in range(wordlength):
            characterinword = wordtocheck[i]
            for j in range(thiswordlength):
                characterinwordfromlist = thiswordfromlist[j]
                if characterinword == characterinwordfromlist:
                    count += 1
                    break
    
        minimumcount = int(0.8*wordlength)

        if count >= minimumcount:
            suggestedwords.append(thiswordfromlist)
    return suggestedwords
    
    
#This function adds a shapefile containing the suburb or locality polygons that the user requests (suburbs)
#It also adds the Open Street Map basemap. It returns the suburb map layer suburb_layer and the basemap layer basemap.
def addfilestomap(suburbs):
    suburb_layer = QgsVectorLayer(suburbs,"Suburbs","ogr")
    basemap_source = "type=xyz&url=https://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0"
    basemap = QgsRasterLayer(basemap_source, 'OpenStreetMap','wms')
    return suburb_layer, basemap

#This function tkaes in the original suburb layer, a text file showing a list of all the zones, with each zone containing a list
#of the suburbs within it and the folder to store all the shapefiles for each zone.
#all_zones, zone_names, localities, suburb_name_attribute, label_attribute
#It returns an array showing all the suburbs by zone, an array showing all the zone names and the column numbers of the suburb names, and
#if different the labels for the suburbs in the maps.
#It returns a modified suburb layer with shows the zone name for each suburb in the attributes.
#The function uses the above checkspellings function to check the spellings of the suburbs in zone_details against the suburb names in the
#suburb shapefile and requests the user to fix any discrepancies.
def modifysuburblayer(suburb_layer, zone_details, output_folder):
    lpth = output_folder + "/Suburbs_With_Zone_Information.shp"
    #Save the suburb_layer shapefile as a new shapefile in the filename defined by lpth
    writer = QgsVectorFileWriter.writeAsVectorFormat(suburb_layer,lpth,'utf-8',driverName='ESRI Shapefile')
    #Add the new saved file to the map as 'suburbs_with_zone_attribute'
    suburbs_with_zone_attribute = QgsVectorLayer(lpth,"Localities","ogr")
    zid = open(zone_details, 'r', encoding='utf-8')
    zone_names = []
    alllinesinfile = zid.readlines()
    numlines = len(alllinesinfile)
    all_suburbs_by_zone = []
    zone_suburbs=[]
    AllSuburbsZoneLists = []
    for i in range(numlines):
        if i == 0:
            zone_names.append(alllinesinfile[i].strip())
        else:
            if alllinesinfile[i-1].isspace() is True:
                zone_names.append(alllinesinfile[i].strip())
                all_suburbs_by_zone.append(zone_suburbs)
                zone_suburbs = []
            else:
                if alllinesinfile[i].isspace() is False:
                    zone_suburbs.append(alllinesinfile[i].strip())
                    AllSuburbsZoneLists.append(alllinesinfile[i].strip)
    #print(AllSuburbsZoneLists)
    all_suburbs_by_zone.append(zone_suburbs)

    
            
    numattributes = 0
    numvalues = 0


    for field in suburbs_with_zone_attribute.fields():
        print (field.name(), field.typeName())
        numattributes += 1

    values = []
    nullvalues = []
    withvalues = []

    i=0
    while i < numattributes:
        values.append(0)
        nullvalues.append(0)
        i += 1

    features = suburbs_with_zone_attribute.getFeatures()
    #For each column count the total number of values and the total number of null values.
    for feature in features:
        attributes = feature.attributes()
        for iatt in range(numattributes):
            variable = attributes[iatt]
            values[iatt]+=1
            if variable == "NULL":
                nullvalues[iatt]+=1

    #Identify all columns full of NULL values (i.e. the number of values is equal to the number of null values.

    for i in range(numattributes):
        if values[i] == nullvalues[i]:
            withvalues.append(0)
        else:
            withvalues.append(1)          

    #delete all columns full of NULL values
    todelete = []
    for iatt in range(numattributes):
        if withvalues == 0:
            todelete.append(iatt)

    suburbs_with_zone_attribute.startEditing()
    suburbs_with_zone_attribute.dataProvider().deleteAttributes(todelete)
    suburbs_with_zone_attribute.dataProvider().addAttributes([QgsField('Zone', QVariant.String)])
    suburbs_with_zone_attribute.updateFields()

    
    numattributes = 0
    string = ''
    allfields = []
    for field in suburbs_with_zone_attribute.fields():
        allfields.append(str(field.name()))
        string = string + str(numattributes) + ". " + str(field.name()) + "\n"
        if field.name() == 'Zone':
            zref = numattributes
        numattributes += 1

    #Ask the user for the column that contains the suburb names
    q = "What field is the suburb names?\n" + string
    sref,ok = QInputDialog().getInt(None, "Column containing the suburb names", q)
    suburb_name_attribute = allfields[sref]

    #Store all suburb names from the suburb layer in an array
    AllSuburbsLocalities = []
    features = suburbs_with_zone_attribute.getFeatures()
    for feature in features:
        attributes = feature.attributes()
        suburbname = attributes[sref]
        AllSuburbsLocalities.append(suburbname)

    nsubzl = len(AllSuburbsZoneLists)
    nsubl = len(AllSuburbsLocalities)
    insuburblist = []
   
    #Identify whether each suburb from the zone_details file is in the suburb layer names list (1) or not (0).
    for i in range(nsubzl):
        count = 0
        for j in range(nsubl):
            if AllSuburbsZoneLists[i] == AllSuburbsLocalities[j]:
                count += 1
                insuburblist.append(count)
            else:
                insuburblist.append(count)
                
    #If the suburb from the zone suburbs file is not in the suburb layer list, ask the user to correct spelling by
    #       a). Identify the word from a list and return a number for the correct option; or
    #       b). If not possible for the function to identify alternatives keep prompting the user to type in a spelling until the word
    #           appears on the list.
    for i in range(nsubzl):
        if insuburblist == 0:
            suggestedwords = checkspellings(AllSuburbsZoneLists[i], AllSuburbsLocalities)
            numsuggestions = len(suggestedwords)
            if numsuggestions > 0:
                string = str(AllSuburbsZoneLists[i]) + " is not a suburb or just not correctly spelt!\nChoose the right replacement from below\n"
                c = len(suggestedwords)
                for j in len(c):
                    string = string + str(j) + ". " + str(suggestedwords[j])
                wordpos,ok = QInputDialog().getInt(None, "Incorrect spelling" , string)
                AllSuburbsZoneLists[i] = suggestedwords[wordpos]
                insuburblist[i] = 1
            else:
                while insuburblist[i] == 0:
                    string = str(AllSuburbsZoneLists[i]) + " is not a suburb or just not correctly spelt!\nThere are so suggestions so type in a replacement\n"
                    word,ok = QInputDialog().getText(None, "Incorrect spelling" , string)
                    AllSuburbsZoneLists[i] = word
                    for k in range(nsub1):
                        if AllSuburbsZoneLists[i] == AllSuburbsLocalities[j]:
                            insuburblist[i] = 1
                    
                                                    
            
                    
    #Ask the user if the labels they want in the map are from the same column as the suburb names. And if not ask the user what column contains
    #those labels.
    mb = QMessageBox()
    mb.setText("Is this the same field as the suburb labels?")
    mb.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return_value = mb.exec()
    
    if return_value == QMessageBox.No:
        lref,ok = QInputDialog().getInt(None, "Field containing the suburb labels", "What field contains the labels?\n"+string)
        label_attribute = allfields[lref]
    else:
        label_attribute = suburb_name_attribute

    numzones = len(zone_names)

    #Allocate the zone name to each suburb in the layer in the attribute table
    idx = 0
    for izone in all_suburbs_by_zone:
        numzonesuburbs = len(izone)
        zfid = []
        features = suburbs_with_zone_attribute.getFeatures()
        for feature in features:
            attributes = feature.attributes()
            suburbname = attributes[sref]
            if suburbname in izone:
                zonenum="ZONE "+ str(zone_names[idx])
                suburbs_with_zone_attribute.changeAttributeValue(feature.id(),zref,zonenum)
                                       
        idx+=1

    #Save the changes to the layer
    suburbs_with_zone_attribute.commitChanges
    print(zone_names)
                
    return all_suburbs_by_zone, zone_names, suburbs_with_zone_attribute, suburb_name_attribute, label_attribute
    

#The function below takes in the edited suburb layer along with the list of the zone names and the directory of the output folder
#to save the shapefiles, one containing the boundary and one containing all the suburbs for each zone.
#For each zone the filenames for each shapefile are added to either the zone_boundary_files list or the zone_suburb_files list which are returned to the user
def createmapshapefiles(output_folder, zone_names, suburbs_with_zone_attribute):
    numzones = len(zone_names)
    path = output_folder + "/FreightZones.shp"
    freight_zones_layer = processing.run("native:collect",{'INPUT':suburbs_with_zone_attribute,'FIELD':['Zone'],'OUTPUT':path})
    zone_boundary_files = []
    zone_suburb_files = []
    print("Creating all zone shapefiles")
    for iz in range(numzones):
        value = "ZONE "+ str(zone_names[iz])
        shpf = output_folder + "/Zone"+ str(zone_names[iz]) + ".shp"
        #print(shpf)
        shpfs = output_folder + "/SuburbsZone"+ str(zone_names[iz]) + ".shp"
        zone_boundary_files.append(shpf)
        zone_suburb_files.append(shpfs)
        zone_lyr = processing.run("native:extractbyattribute", {'INPUT':suburbs_with_zone_attribute,'FIELD':'Zone','OPERATOR':0,'VALUE':value,'OUTPUT':shpfs})
        zone_boundary = processing.run("native:dissolve", {'INPUT':shpfs,'FIELD':[],'OUTPUT':shpf})
    return zone_boundary_files, zone_suburb_files

#The function below creates the maps for each zone and saves them as PDF files.
#It takes in the name of each of the zone's boundary shapefile (zone_boundary) and the zone's suburbs shapefile (suburbs_within_zone)
#It takes the map canvas, the directory to store all PDF maps, the list of the zone names and the columns of the suburb names for each zone
#to be displayed in the map. It also takes in the array bshowing all the suburbs for each zone.
def createmaps(canvas, output_folder, zone_boundary, suburbs_within_zone , zone_names, label_attribute, all_suburbs_by_zone):    
    single_symbol_renderer2 = zone_boundary.renderer()
    symbol_fz2 = single_symbol_renderer2.symbol()
    #Set fill colour
    symbol_fz2.setColor(QColor.fromRgb(121,61,244))
    #Set fill style
    symbol_fz2.symbolLayer(0).setBrushStyle(Qt.BrushStyle(Qt.NoBrush))#Set stroke colour
    symbol_fz2.symbolLayer(0).setStrokeColor(QColor(121,61,244))
    symbol_fz2.symbolLayer(0).setStrokeWidth(2)
    #Set transparency
    symbol_fz2.setOpacity(100)
    #Refresh
    zone_boundary.triggerRepaint()

    single_symbol_renderer = suburbs_within_zone.renderer()
    symbol_fz = single_symbol_renderer.symbol()
    #Set fill colour
    symbol_fz.setColor(QColor.fromRgb(124,10,2))
    #Set fill style
    symbol_fz.symbolLayer(0).setBrushStyle(Qt.BrushStyle(Qt.NoBrush))#Set stroke colour
    symbol_fz.symbolLayer(0).setStrokeColor(QColor.fromRgb(124,10,2))
    #Set transparency
    symbol_fz.setOpacity(100)
    #Refresh
    suburbs_within_zone.triggerRepaint()

    #Set the map extent on the screen
    extent = zone_boundary.extent() 
    canvas.setExtent(extent)
    

    layer_settings  = QgsPalLayerSettings()
    text_format = QgsTextFormat()

    #Set the text format for the map labels
    text_format.setFont(QFont("Arial", 11))
    text_format.setSize(11)
    text_format.setColor(QColor.fromRgb(169,169,169))

    #Add a buffer around the text characters
    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(1)
    buffer_settings.setColor(QColor("white"))

    text_format.setBuffer(buffer_settings)
    layer_settings.setFormat(text_format)

    #Set the field to be labelled
    layer_settings.fieldName = label_attribute
    layer_settings.placement = 0

    layer_settings.enabled = True
    layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    #Enable the labels to be shown
    suburbs_within_zone.setLabelsEnabled(True)
    suburbs_within_zone.setLabeling(layer_settings)
    #Refresh
    suburbs_within_zone.triggerRepaint()

    project = QgsProject.instance()
    #Create the map layout
    manager = project.layoutManager()
    layoutName = 'Layout1'
    layouts_list = manager.printLayouts()
    #Remove any duplicate layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)

    #Set the map extent, using the longitude and latitude extremes for the zone boundary layer
    extt = zone_boundary.extent()
    xmin = extt.xMinimum()
    xmax = extt.xMaximum() 
    ymin = extt.yMinimum()
    ymax = extt.yMaximum()

    #Calculate the length, width and the ratio of the length to width of the zone boundary shape
    length = ymax - ymin
    width = xmax - xmin
    ratio = length/width


    #If the ratio of the length to width is greater than one, than the map will be in a potrait layout.
    if ratio > 1:
        #Initalize the map frame dimensions = 280 by 390 for potrait
        mapwidth = 280
        maplength = 370

        #Scale the map width according to the defined length of the map
        scaledmapwidth = int(maplength/ratio)
        if scaledmapwidth > mapwidth:
            scaledownfactor = mapwidth/scaledmapwidth
            maplength = maplength*scaledownfactor
        else:
            mapwidth = scaledmapwidth    
            
        print("Zone " + str(zone_names) + " will be a Portrait layout")
        pc = layout.pageCollection()
        pc.page(0).setPageSize('A3',QgsLayoutItemPage.Orientation.Portrait)
        manager.addLayout(layout)

        #Create map item in the layout
        map = QgsLayoutItemMap(layout)
        map.setRect(20, 20, 5, 5)
        
        ms = QgsMapSettings()
        #Set layers to be mapped
        ms.setLayers([suburbs_within_zone,zone_boundary])
        #Set the coordinate extent of the map and relative scale
        rect = QgsRectangle(ms.fullExtent())
        rect.scale(1)
        ms.setExtent(rect)
        map.setExtent(rect)
        map.setBackgroundColor(QColor(255, 255, 255, 0))
        layout.addLayoutItem(map)

        #Adjust the position and size of the map
        map.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(mapwidth, maplength, QgsUnitTypes.LayoutMillimeters))
        map.setFrameEnabled(True)

        #Set up the map legend
        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Legend")
        layerTree = QgsLayerTree()
        #Add layers to include in the legend
        layerTree.addLayer(zone_boundary)
        layerTree.addLayer(suburbs_within_zone)
        legend.model().setRootGroup(layerTree)
        layout.addLayoutItem(legend)

        #Calculate and adjust position of the legend relative to the map frame
        if mapwidth < 240:
            posx = mapwidth + 6
            posy = 20
        else:
            posx = 10
            posy = maplength + 21

        legend.attemptMove(QgsLayoutPoint(posx, posy, QgsUnitTypes.LayoutMillimeters))
        legend.setFrameEnabled(True)
 
        #Set up the scalebar
        scalebar = QgsLayoutItemScaleBar(layout)
        #Set up the scalebar type, units and other details
        scalebar.setStyle('Line Ticks Up')
        scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
        scalebar.setNumberOfSegments(1)
        scalebar.setNumberOfSegmentsLeft(0)
        scalebar.setUnitsPerSegment(1)
        scalebar.setLinkedMap(map)
        scalebar.setUnitLabel('km')
        scalebar.setFont(QFont('Arial', 14))
        #Refresh
        scalebar.update()
        #Add scalebar to map and calculate position to move it to
        layout.addLayoutItem(scalebar)
        if mapwidth < 240:
            posx = mapwidth + 6
            posy = int(mapwidth/2) + 20
        else:
            posx = int(mapwidth/2)
            posy = maplength + 21
        scalebar.attemptMove(QgsLayoutPoint(posx, posy, QgsUnitTypes.LayoutMillimeters))
        scalebar.setFrameEnabled(True)

        #qgis.core.QgsLayoutNorthArrowHandler(parent: QObject)

        #C:\Program Files (x86)\QGIS 3.14\apps\grass\grass78\gui\images\symbols\n_arrows.png
        #Add north arrow
        if mapwidth < 240:
            posx = mapwidth + 11
            posy = maplength - 10
        else:
            posx = mapwidth - 10 
            posy = maplength + 26

        northarrow = QPolygonF()
        northarrow.append(QPointF(posx, posy))
        northarrow.append(QPointF(posx-4, posy+8))
        northarrow.append(QPointF(posx, posy+6))
        northarrow.append(QPointF(posx+4, posy+8))

        northarrowitem = QgsLayoutItemPolygon(northarrow, layout)
        layout.addLayoutItem(northarrowitem)
        northlabel = QgsLayoutItemLabel(layout)
        northtext = "N"
        northlabel.setText(northtext)
        northlabel.setFont(QFont('Arial',12))
        northlabel.adjustSizeToText()
        layout.addLayoutItem(northlabel)
        northlabel.attemptMove(QgsLayoutPoint(posx-1, posy+9, QgsUnitTypes.LayoutMillimeters))

        #Set up and add the map title
        title = QgsLayoutItemLabel(layout)
        text_lyr = "Zone "+str(zone_names)
        title.setText(text_lyr)
        title.setFont(QFont('Arial', 24))
        title.adjustSizeToText()
        layout.addLayoutItem(title)
        title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))
        
        #Save and export the layout as PDF
        layout = manager.layoutByName(layoutName)
        exporter = QgsLayoutExporter(layout)

        print("Saving map as PDF file")
        fn = output_folder + '/Zone' + str(zone_names) +'.pdf'
        exporter.exportToPdf(fn, QgsLayoutExporter.PdfExportSettings())
    #If the width is at greater than or equal to the length of the zone boundary than the zone will be mapped on a landscape page.
    else:
        #Inital map frame dimensions = 380 by 260 for the landscape map
        mapwidth = 380
        maplength = 260

        #Scale the map width to the defined width
        scaledmapwidth = int(maplength/ratio)
        if scaledmapwidth > mapwidth:
            scaledownfactor = mapwidth/scaledmapwidth
            maplength = maplength*scaledownfactor
        else:
            mapwidth = scaledmapwidth
            
        print("Zone " + str(zone_names) + " will be a Landscape layout")
        pc = layout.pageCollection()
        pc.page(0).setPageSize('A3',QgsLayoutItemPage.Orientation.Landscape)
        manager.addLayout(layout)
    
  
        #Create map item in the layout
        map = QgsLayoutItemMap(layout)
        map.setRect(20, 20, 5, 5)
        

        ms = QgsMapSettings()
        #Set layers to be mapped
        ms.setLayers([suburbs_within_zone,zone_boundary])
        #Set the coordinate extent of the map
        rect = QgsRectangle(ms.fullExtent())
        rect.scale(1)
        ms.setExtent(rect)
        map.setExtent(rect)
        map.setBackgroundColor(QColor(255, 255, 255, 0))
        layout.addLayoutItem(map)

        #Adjust the position and size of the map
        map.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(mapwidth, maplength, QgsUnitTypes.LayoutMillimeters))
        map.setFrameEnabled(True)

        #Create the map legend
        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Legend")
        layerTree = QgsLayerTree()
        #Add layers to include in the legend
        layerTree.addLayer(zone_boundary)
        layerTree.addLayer(suburbs_within_zone)
        legend.model().setRootGroup(layerTree)
        layout.addLayoutItem(legend)
        #Calculate and adjust the position of the legend relative to the map
        if mapwidth < 380:
            posx = mapwidth + 6
            posy = 20
        else:
            posx = 10
            posy = maplength + 21

        legend.attemptMove(QgsLayoutPoint(posx, posy, QgsUnitTypes.LayoutMillimeters))
        legend.setFrameEnabled(True)

        #Create the scalebar
        scalebar = QgsLayoutItemScaleBar(layout)
        #Set up the format and other details of the scalebar
        scalebar.setStyle('Line Ticks Up')
        scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
        scalebar.setNumberOfSegments(1)
        scalebar.setNumberOfSegmentsLeft(0)
        scalebar.setUnitsPerSegment(1)
        scalebar.setLinkedMap(map)
        scalebar.setUnitLabel('km')
        scalebar.setFont(QFont('Arial', 14))
        scalebar.update()
        #Add scalebar to the map
        layout.addLayoutItem(scalebar)
        #Calculate the position of the scalebar relative to the map and adjust to it
        if mapwidth < 380:
            posx = mapwidth + 6
            posy = int(maplength/2) + 20
        else:
            posx = int(mapwidth/2) + 10
            posy = maplength + 21
        scalebar.attemptMove(QgsLayoutPoint(posx, posy, QgsUnitTypes.LayoutMillimeters))
        scalebar.setFrameEnabled(True)

        #Add north arrow
        if mapwidth < 380:
            posx = mapwidth + 11
            posy = maplength - 10
        else:
            posx = mapwidth - 10 
            posy = maplength + 26

        northarrow = QPolygonF()
        northarrow.append(QPointF(posx, posy))
        northarrow.append(QPointF(posx-4, posy+8))
        northarrow.append(QPointF(posx, posy+6))
        northarrow.append(QPointF(posx+4, posy+8))

        northarrowitem = QgsLayoutItemPolygon(northarrow, layout)
        layout.addLayoutItem(northarrowitem)
        northarrowitem = QgsLayoutItemPolygon(northarrow, layout)
        layout.addLayoutItem(northarrowitem)
        northlabel = QgsLayoutItemLabel(layout)
        northtext = "N"
        northlabel.setText(northtext)
        northlabel.setFont(QFont('Arial',12))
        northlabel.adjustSizeToText()
        layout.addLayoutItem(northlabel)
        northlabel.attemptMove(QgsLayoutPoint(posx-1, posy+9, QgsUnitTypes.LayoutMillimeters)) 
 
        #Create the map title
        title = QgsLayoutItemLabel(layout)
        text_lyr = "Zone "+str(zone_names)
        title.setText(text_lyr)
        title.setFont(QFont('Arial', 24))
        title.adjustSizeToText()
        layout.addLayoutItem(title)
        title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))

        #Save layout and save map as a PDF
        layout = manager.layoutByName(layoutName)
        exporter = QgsLayoutExporter(layout)
                
        print("Saving map as PDF file")
        fn =output_folder + '/Zone' + str(zone_names) +'.pdf'
        exporter.exportToPdf(fn, QgsLayoutExporter.PdfExportSettings())
                          

    return fn


class ClickBox(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        description = QLabel()
        program_description = 'This is a program that creates maps of zones based on\n a user defined suburb shapefile and a\n textfile showing the list of zones with the suburbs\n in each zone.\n\n The maps are saved as PDF files to the location \nspecified by the user.'
        description.setText(program_description)
        label1 = QLabel()
        label1.setText("Select the following")
        self.buttonbox1 = QPushButton("Localities Shapefile")
        self.buttonbox1.clicked.connect(self.run1)
        self.buttonbox2 = QPushButton("Zone Suburb Lists")
        self.buttonbox2.clicked.connect(self.run2)
        self.buttonbox3 = QPushButton("Output Folder")
        self.buttonbox3.clicked.connect(self.run3)
        self.buttonboxhelp = QPushButton('Help')
        self.buttonboxhelp.clicked.connect(self.runHelp)
        self.buttonboxOK = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonboxOK.accepted.connect(self.runOK)
        tblabel1 = QLabel()
        tblabel1.setText("Suburb shapefile")
        tblabel2 = QLabel()
        tblabel2.setText("Zone details file")
        tblabel3 = QLabel()
        tblabel3.setText("Output folder")
        self.textbox1 = QLineEdit()
        self.textbox2 = QLineEdit()
        self.textbox3 = QLineEdit()
        self.layout.addWidget(description)
        self.layout.addWidget(label1)
        self.layout.addWidget(self.buttonbox1)
        self.layout.addWidget(self.buttonbox2)
        self.layout.addWidget(self.buttonbox3)
        self.layout.addWidget(tblabel1)
        self.layout.addWidget(self.textbox1)
        self.layout.addWidget(tblabel2)
        self.layout.addWidget(self.textbox2)
        self.layout.addWidget(tblabel3)
        self.layout.addWidget(self.textbox3)
        self.layout.addWidget(self.buttonboxhelp)
        self.layout.addWidget(self.buttonboxOK)
        self.setLayout(self.layout)
    def run1(self):
        suburbs = QFileDialog.getOpenFileName(QFileDialog(),"Open shapefile showing all the suburbs","C:/Users/Azzla/Documents/","*.shp")
        self.textbox1.setText(suburbs[0])
    def run2(self):
        zone_details = QFileDialog.getOpenFileName(QFileDialog(),"Open textfile showing all the zone names and their suburbs","C:/Users/Azzla/Documents/","*.txt")
        self.textbox2.setText(zone_details[0])
    def run3(self):
        output_folder = str(QFileDialog.getExistingDirectory(self, "Select directory to store all the maps"))
        self.textbox3.setText(output_folder)
    def runHelp(self):
        #print('ok')
        current_directory = os.getcwd()
        read_me_file = current_directory + "/ReadMe.txt"
        os.system('notepad.exe ' + read_me_file)
    def runOK(self):
        #print(self.textbox1.text(), self.textbox2.text(), self.textbox3.text())
        self.textbox1.setEnabled(False)
        self.textbox2.setEnabled(False)
        self.textbox3.setEnabled(False)
        self.buttonbox1.setEnabled(False)
        self.buttonbox2.setEnabled(False)
        self.buttonbox3.setEnabled(False)
        self.buttonboxOK.setEnabled(False)
        suburbs = self.textbox1.text()
        zone_details = self.textbox2.text()
        output_folder = self.textbox3.text()
        canvas = qgis.utils.iface.mapCanvas()
        registry = QgsProject.instance()
        suburb_layer,basemap = addfilestomap(suburbs)
        all_suburbs_by_zone, zone_names, suburbs_with_zone_attribute, suburb_name_attribute, label_attribute = modifysuburblayer(suburb_layer, zone_details, output_folder)
        registry.addMapLayers([suburb_layer,basemap, suburbs_with_zone_attribute])
        zone_boundary_files, zone_suburb_files = createmapshapefiles(output_folder, zone_names, suburbs_with_zone_attribute)        
        registry.removeMapLayer(suburbs_with_zone_attribute)
        registry.removeMapLayer(suburb_layer)
        numzones = len(zone_names)
        iz = 0
        pdf_file_list = []
        while iz < numzones:
            msg = "Creating map of zone " + str(zone_names[iz])
            print(msg)
            shpf = zone_boundary_files[iz]
            shpfs = zone_suburb_files[iz]
            
            zone_boundary = QgsVectorLayer(shpf,"Zone Boundary","ogr")
            suburbs_within_zone = QgsVectorLayer(shpfs,"Suburbs in Zone","ogr")
            print(all_suburbs_by_zone[iz])
            print(zone_names[iz])
            #print(zone_suburb_files[iz])
            
            registry.addMapLayers([suburbs_within_zone,zone_boundary])
            pdf_f = createmaps(canvas, output_folder, zone_boundary, suburbs_within_zone, zone_names[iz], label_attribute, all_suburbs_by_zone[iz])
            registry.removeMapLayer(zone_boundary)
            registry.removeMapLayer(suburbs_within_zone)
            pdf_file_list.append(pdf_f)
            print('zone map complete')
            iz += 1
        msg = QMessageBox()
        msg.setText("COMPLETE\nRun again?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return_value = msg.exec()
        if return_value == QMessageBox.Yes:
            self.textbox1.setEnabled(True)
            self.textbox2.setEnabled(True)
            self.textbox3.setEnabled(True)
            self.buttonbox1.setEnabled(True)
            self.buttonbox2.setEnabled(True)
            self.buttonbox3.setEnabled(True)
            self.buttonboxOK.setEnabled(True)
        else:
            sys.exit()
            

buttons = ClickBox()
buttons.show()





    
