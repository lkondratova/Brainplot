import os, importlib, matplotlib, pandas as pd, numpy as np, matplotlib.pyplot as plt
import time
from PIL import Image, ImageDraw, ImageColor, ImageFilter, ImageFont

def initialization():
    global dirpath, readings, animal, templates, left, right, areas, areas1, urls, y
    global ferret, human, macaque, mouse, mouse_allen, opossum, rat  
    urls = {'macaque':'https://scalablebrainatlas.incf.org/macaque/CBCetal15', 
        'mouse_allen':'https://scalablebrainatlas.incf.org/mouse/ABA_v3',
        'mouse':'https://scalablebrainatlas.incf.org/mouse/WHS12',
       'rat':'https://scalablebrainatlas.incf.org/rat/CBWJ13_age_P80',
       'human':'https://scalablebrainatlas.incf.org/human/NMM1103',
       'ferret':'https://scalablebrainatlas.incf.org/ferret/HSRetal17',
       'opossum':'https://scalablebrainatlas.incf.org/opossum/OPSM14'}    
    dirpath = os.getcwd()
    readings=[]
    templates = []
    left=None
    right=None
#set up variable 'areas'
#variable dirpath - str, current location
#areas_available(animal) - a function to receive all areas available for the chosen animal.
def areas_available(animal, templates, i):
    global t, names
    module_to_import = "template_container_"+animal+".events"
    module_to_import1= "template_container_"+animal+".variables"
    y = __import__(module_to_import, globals=None, locals=None, 
                   fromlist=['RGB_TO_ACR', 'ACR_TO_FULL', 'template_dict'])
    x= __import__(module_to_import1, globals=None, locals=None, 
                   fromlist=['events_by_slices'])
    templ = y.template_dict
    t=templ[templates[i]]
    slice_events = x.events_by_slices[t] #this variable contains all the events present on the chosen template.
    names = {}
    for v in range(len(slice_events)):
        print(slice_events[v])
        if isinstance(slice_events[v], str):
            if slice_events[v] in y.RGB_TO_ACR.keys():
                names[slice_events[v]]=[(y.RGB_TO_ACR[slice_events[v]])]  
                if y.RGB_TO_ACR[slice_events[v]] in y.ACR_TO_FULL.keys():
                    names[slice_events[v]].append(y.ACR_TO_FULL[y.RGB_TO_ACR[slice_events[v]]])
        else:
            pass


    
def template_list():
        templates_done=False
        while templates_done == False:
            print('Enter slice #' + str(len(templates)+1) + ' that you want to use in your visualisation (use the value that is showing in parentheses):')
            template = input() #!!!! pick the template from the window
            #? print('Enter slice #' + str(len(templates)+1) + ' that you want to use in your visualisation (use the value that is showing in parentheses):')
            templates.append(template)
            print ('You selected slices # '+ ', '.join([str(elem) for elem in templates]) + ' as templates.')
        #open all templates that will be used (from variable 'templates') and save in 'output' folder
        #!!! probably just open and keep in cash.
        #!!!!!!!!!!!!
        open_templates(animal, templates)

        areas1 = []
        #make multichoice menu for each template in separate window
        areas_input(templates)

#create variable representing slice numbers in files. 
#templates: variable that holds slice numbers as they are in parentheses on site.
#templ: variable that holds corresponding slice numbers as they appear in files and in original variables.
def create_templ(animal, templates):
    global templ
    templ = []
    for i in range(len(templates)):
        slice_num = globals()[animal][int(templates[i])]
        templ.append(slice_num)
        
#open all templates that will be used (from variable 'templates')
def open_templates(animal, templates):
    global dirpath
    dirpath = os.getcwd() #!!!!!!!!! ask user where to store output, call variable output (ask at the first step)
    for i in range(len(templates)):
        filename = str(dirpath+'/template_container_'+animal+'/slice_numbers/'+templates[i]+'.png') #at this point templates won't be #stored
def areas_input(templates):
    global areas1
    areas1 = []
    areas=[]
    for i in range(len(templates)):
        #create multichoice menu with the template on the top, number of the template, and all the areas available on this template.
        area = input()
        areas.append(area.split(','))
    for i in range(len(areas)):
        temp = []
        for j in range(len(areas[i])):
            x = str(areas[i][j]).split('$')
            temp.append(x)
        areas1.append(temp)

#************************************************

def areas_viz():
    #create dataframe to visualize the templates and areas to be applied
    if os.path.exists(output_dirpath+"/0_figures.html") == True:
        os.remove(output_dirpath+"/0_figures.html")
    html_file= open(output_dirpath+"/0_figures.html","a")
    html_file.write('<h1>Auto Input</h1>\n')
    module_to_import = "template_container_"+animal+".events"
    y = __import__(module_to_import, globals=None, locals=None, fromlist=['RGB_TO_ACR', 'ACR_TO_FULL'])
    acr_to_full = dict((k.lower(), v.lower()) for k,v in y.ACR_TO_FULL.items())
    data = []
    data1 = []
    col = ['template #']
    #check if areas items are the same size and if they are present in the atlas
    for i in range(len(areas1)):
        if len(areas1[i])>1:
            for k in range(len(areas1)-1):
                if len(areas1[k]) != len(areas1[k+1]):
                    print('The areas entered are not the same size for all templates. To enter the correct areas run the program again')
                    break
        for j in range(len(areas1[i])):
            for k in range(len(areas1[i][j])):
                a = areas1[i][j][k]
                if a.startswith(' '):
                    areas1[i][j][k] = a[1:]
                    a = a[1:]
                if a.lower() != 'n/a' and a.lower() not in acr_to_full.keys() and a.lower() not in acr_to_full.values() and a!='' and a!=' ':
                    print(list(a))
                    print(type(a))
                    while True:
                        print ("Area "+a+" is not available for "+animal+". Do you want to enter another area name? (y/n)")
                        answer = input()
                        if answer.lower()=='y' or answer.lower =='yes':
                            print("Enter the new area:")
                            a = input()
                            if a.lower() in acr_to_full.keys() or a.lower() in acr_to_full.values() or a.lower() == n/a:
                                break
                        if answer.lower()=='n' or answer.lower() == 'no':
                            break
    print()
    print('All areas found. Creating matrix for visualization.')

    for i in range(len(areas1[0])):
        col.append('column_'+str(i+1))
    for i in range(len(templates)):
        data.append([templates[i]])
        data1.append([templates[i]])
        for j in range(len(areas1[i])):
            if areas1[i][j] == ['n/a'] or areas1[i][j] == ['N/A'] or areas1[i][j] == [' n/a'] or areas1[i][j] == [' N/A']:
                data[i].append('-')
                data1[i].append(areas1[i][j])
            else:
                data[i].append('+')
                data1[i].append(areas1[i][j])

    try:
        df = pd.DataFrame(data, columns = col)
        df1 = pd.DataFrame(data1, columns = col)
    except (ValueError):
        print('Cannot print matrix for areas to be applied. Please check entered areas.')
        pass
    print(df)
    html = df.to_html()
    html_file.write(html+'\n')
    html_file.write('<h1>***</>\n')
    html = df1.to_html()
    html_file.write(html+'\n')
    html_file.close()
    print('More visualization for the areas and templates stored in output/figures.html')
    print('Converting areas to the corresponding events. ')

#*********************************************************************


def labels_transformation(animal, slice_number, area_required):
    global events, ferret, human, macaque, mouse, mouse_allen, opossum, rat, module_to_import, module_to_import_1, y
    module_to_import = "template_container_"+animal+".events"
    module_to_import_1 = "template_container_"+animal+".variables"
    y = __import__(module_to_import, globals=None, locals=None, fromlist=['RGB_TO_ACR', 'ACR_TO_FULL','ACR_TO_PARENT'])
    #slice_num = globals()[animal][int(slice_number)]
    area_required = str(area_required).lower()
    rgb_to_acr = dict((k.lower(), v.lower()) for k,v in y.RGB_TO_ACR.items())
    acr_to_full = dict((k.lower(), v.lower()) for k,v in y.ACR_TO_FULL.items())
    inverted_acr = {v: k for k, v in rgb_to_acr.items()}
    inverted_full = {v: k for k, v in acr_to_full.items()}
    inverted_agb = {v: k for k, v in rgb_to_acr.items()}
    found_event = False
    if area_required in rgb_to_acr.values():
        events = (inverted_agb[area_required].upper())
        found_event=True
    elif area_required in acr_to_full.keys() and not found_event:
        events=(inverted_acr[area_required].upper())
        found_event=True
    elif area_required in acr_to_full.values() and not found_event:
        suba = inverted_full[area_required]
        if inverted_acr[suba].upper() not in events:
            events=(inverted_acr[suba].upper())
    elif area_required == 'n/a' or area_required == ' n/a':
        events='' 
        
def identify_events():
    global events, events1, y, brain_regions, templ
    events = ''
    #labels_transformation(animal, slice_number, area_required)
    #fill the list events1 with required events using the structure corresponding to areas1   

    events1 = []
    module_to_import_2 = "template_container_"+animal+".template_container_"+animal
    brain_regions=__import__(module_to_import_2, globals=None, locals=None, fromlist=['BRAIN_REGIONS', 'BRAIN_SLICES'])
    for i in range(len(templates)):
        brain_slice = brain_regions.BRAIN_SLICES[templ[i]]
        events1.append([])
        for j in range(len(areas1[i])):
            events1[i].append([])
            for k in range(len(areas1[i][j])):
                labels_transformation(animal, templ[i], areas1[i][j][k])
                if events not in brain_regions.BRAIN_REGIONS and events in y.RGB_TO_ACR:
                    events=''
                    for key in y.ACR_TO_PARENT:
                        if y.ACR_TO_PARENT[key] == areas1[i][j][k]:
                            labels_transformation(animal, templ[i], key)
                            if events in brain_slice:
                                events1[i][j].append(events)
                                events=''
                else:
                    events1[i][j].append(events)
                    events = ''
    print('Events identified. Converting to pixel coordinates.')

#**********************************************************************

def to_pixel_coordinates():
    global labels_l, animal, events1, templates, label, name, templ
    # this chunk creates the list that is identical to events1 by its structure but is filled with pixel coordinates 
    #instead of events names.
    labels_l = []
    for i in range(len(templates)):
        labels_l.append([])
        globals()['module_to_import_z'] = 'template_container_'+animal+'.labels.slice_'+str(templ[i])
        for j in range(len(events1[i])):
            labels_l[i].append([])
            for k in range(len(events1[i][j])):
                if events1[i][j][k] == '':
                    labels_l[i][j].append('')
                else:
                    globals()['name']='coordinates_'+str(events1[i][j][k])
                    globals()['label'] = importlib.import_module(module_to_import_z)
                    s = getattr(label, name)
                    labels_l[i][j].append(s)

    print('Done! Pixel coordinates pulled up.')
    
#open .csv file. 
# values.csv - for the functions whole_*
# values1.csv(left) and values2.csv(right) for two_sided_*

def open_whole(colormap):
    global data_dirpath, output_dirpath, pd, values_normalized, min_max, val, html_file
    try:
        values=pd.read_csv(data_dirpath, index_col=0)
        ds=values.describe()
        ds_to_html = ds.to_html()
        html_file= open(output_dirpath+"/output/0_figures.html","a")
        html_file.write('<h1>Descriptive Statistics For <i>values.csv</i></h1>\n')
        html_file.write(ds_to_html+'\n')
        plt.imshow(values, cmap=colormap)
        plt.colorbar()
        plt.xticks(range(len(values)),values.columns, rotation=90)
        plt.yticks(range(len(values)), values.index)
        plt.savefig(output_dirpath+'/colormap.jpg', bbox_inches='tight')
        
        html_file.write('<img src = ' + output_dirpath+'/colormap.jpg>\n')
        html_file.close()
        #os.remove(dirpath+'colormap.png')
        plt.show()
        print("Identified file 'values.csv' \n")
        #print(values.describe(), ' \n', 'Values:', values.plot.box(rot=45))
    except(TypeError, pd.errors.ParserError):
        return('Cannot open "values.csv".')
        pass
    except(FileNotFoundError, IOError):
        return("Cannot find 'values.csv'.")
        pass
    except(pd.errors.DtypeWarning):
        return("Data types in 'values.csv' are not uniform.")
        pass
    max_col=values.max()
    max_val=max(max_col, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    min_col=values.min()
    min_val=min(min_col, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    values_normalized=(values-min_val)/(max_val-min_val)
    min_max=[min_val, max_val]
    val = [values_normalized]
    


    
def open_two_sided(colormap):
    global data_dirpath, data_dirpath2, output_dirpath, pd, values1_normalized, values2_normalized, min_max, val
    try:
        values1=pd.read_csv(data_dirpath, index_col=0)
        ds=values1.describe()
        ds_to_html = ds.to_html()
        html_file= open(data_dirpath+"/0_figures.html","a")
        
        
        html_file.write('<h1>Descriptive Statistics For <i>values1.csv</i></h1>\n')
        html_file.write(ds_to_html+'\n')
        plt.imshow(values1, cmap=colormap)
        plt.colorbar()
        plt.xticks(range(len(values1)),values1.columns, rotation=90)
        plt.yticks(range(len(values1)), values1.index)
        plt.savefig(output_dirpath+'/colormap1.jpg', bbox_inches='tight')
        html_file.write('<img src = ' + output_dirpath+'/colormap1.jpg>\n')
        plt.show()
        print("Identified file 'values1.csv' \n")
        #print(values1.describe(), ' \n')
    except(TypeError, pd.errors.ParserError):
        print('Cannot open "values1.csv".')
        pass
    except(FileNotFoundError, IOError):
        print("Cannot find 'values1.csv'.")
        pass
    except(pd.errors.DtypeWarning):
        print("Data types in 'values1.csv' are not uniform.")
        pass
    try:
        values2=pd.read_csv(data_dirpath, index_col=0)
        ds2=values2.describe()
        ds2_to_html = ds2.to_html()
        html_file= open(output_dirpath+"/0_figures.html","a")
        html_file.write('<h1>Descriptive Statistics For <i>values2.csv</i></h1>\n')
        html_file.write(ds2_to_html+'\n')
        plt.imshow(values2, cmap=colormap)
        plt.colorbar()
        plt.xticks(range(len(values2)),values2.columns, rotation=90)
        plt.yticks(range(len(values2)), values2.index)
        plt.savefig(output_dirpath+'/colormap2.jpg', bbox_inches='tight')
        html_file.write('<img src = ' + output_dirpath+'/colormap2.jpg>\n')
        plt.show()
        print("Identified file 'values2.csv' \n")
        #print(values2.describe(), ' \n') 
    except(TypeError, pd.errors.ParserError):
        print('Cannot open "values2.csv".')
        pass
    except(FileNotFoundError, IOError):
        print("Cannot find 'values2.csv'.")
        pass
    except(pd.errors.DtypeWarning):
        print("Data types in 'values2.csv' are not uniform.")
        pass
    plt.figure()
    ax1 = plt.gca()
    values1.plot(kind='box', color='blue', ax=ax1, rot=45)
    values2.plot(kind='box', color='yellow', ax=ax1, rot=45)
    html_file.write('<h1>Overlap by Columns. <i>values1</i>: blue & <i>values2</i>: yellow</h1>\n')
    plt.savefig(output_dirpath+'/boxplot.jpg', bbox_inches='tight')
    html_file.write('<img src = ' + output_dirpath+'/boxplot.jpg>\n')
    html_file.close()
    #plt.show()
    max_col1=values1.max()
    max_col2=values2.max()
    min_col1=values1.min()
    min_col2=values2.min()
    max_val1=max(max_col1, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    max_val2=max(max_col2, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    min_val1=min(min_col1, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    min_val2=min(min_col2, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    max_v=max([max_val1, max_val2])
    min_v=min([min_val1, min_val2])
    values1_normalized=(values1-min_v)/(max_v-min_v)
    values2_normalized=(values2-min_v)/(max_v-min_v)
    min_max=[max_v, min_v]
    val = [values1_normalized, values2_normalized]
    
    

#colormaps https://matplotlib.org/3.2.1/tutorials/colors/colormaps.html
#https://matplotlib.org/examples/color/colormaps_reference.html
#function(colormap='viridis', )
#iterate through the all values in the values.csv and create a numpy array with colors from corresponding colormap
#change the 'whole_one_color' function
def whole_colormap(colormap='viridis'):
    global cv2, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont, time
    global labels_list,values_normalized, output_dirpath, dirpath, val, min_max, im_name
    start_time = time.time()
    #colormaps https://matplotlib.org/3.2.1/tutorials/colors/colormaps.html
    #https://matplotlib.org/examples/color/colormaps_reference.html
    #iterate through the all values in the values.csv and create a list with colors from corresponding colormap
    initialization()
    create_templ(animal, templates)
    areas_viz()
    identify_events()
    to_pixel_coordinates()
    
    open_whole(colormap) #open the values.csv file
    print("Coloring templates...")
    cmap=matplotlib.cm.get_cmap(colormap)
    ax = plt.subplot(111)
    im = ax.imshow(np.array(min_max).reshape((2, 1)),cmap=cmap)
    plt.colorbar(im, ax=ax)
    ax.remove()
    plt.savefig(output_dirpath+'/colorbar.png', bbox_inches='tight')
    colors = []
    im_name = list(val[0].index)
    for i in range(len(val)):
        colors.append([])
        shape=val[i].shape
        for row in range(shape[0]):
            colors[i].append([])
            for col in range(shape[1]):
                va = val[i].iloc[row,col]
                rgba = list(cmap(va))
                for c in range(4):
                    rgba[c]=int(rgba[c]*255)
                colors[i][row].append(tuple(rgba))
    #coloring each slice and saving with name from arguments (identifier).
    def color_templ(im_name, slice_no,t):# slice_no is templates[t] from outer loop referring to the index in 'templates'
        global width, height
        identifier=str(im_name) #name is a variable from the outer loop iterating though the index column
        slice_no = str(slice_no) 
        out_dir = os.fsencode(output_dirpath+'/output') 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                label_name=identifier+'_'+slice_no+'_'+str(t)
                templ = Image.open(dirpath+'/template_container_'+animal+'/output/'+slice_no+'_'+str(t)+'.png')
                width, height = templ.size
                templ1=Image.new('RGBA', (width, height), (255,255,255,0))
                for i in range(len(labels_l[t])): # t is the variable from outer loop referring to the index in 'templates'
                    for k in range(len(labels_l[t][i])): #iterating within areas for each sample (aka rows)
                        event = labels_l[t][i][k]
                        for xy in range(len(event)):
                            if event == '':
                                pass
                            else:
                                pixel_w = event[xy][0]
                                pixel_h = event[xy][1]
                                templ1.putpixel((pixel_w, pixel_h), colors[0][name][i])
                                templ1.putpixel((pixel_w-1, pixel_h-1), colors[0][name][i])
                                templ1.putpixel((pixel_w+1, pixel_h+1), colors[0][name][i])
                                templ1.putpixel((pixel_w-1, pixel_h+1), colors[0][name][i])
                                templ1.putpixel((pixel_w+1, pixel_h-1), colors[0][name][i])
                templ1 = templ1.filter(ImageFilter.GaussianBlur(radius=1))
                templ1.palette = None
                templ.paste(templ1, (0,0), templ1)
                templ.save(str(output_dirpath+'/output/'+label_name+'.png'), 'PNG')

    for name in range(len(im_name)):
        for t in range(len(templates)):
            color_templ(im_name[name], templates[t],t)
    #saving .pdf
    #variable im_name is a list that holds names for all samples from the file values.csv as strings
    #width, height go from the previous function and are the width and height of the template and saved images
    if not os.path.exists(output_dirpath +'/output/pdf'):
        os.makedirs(output_dirpath+'/output/pdf')
    for i in range(len(im_name)):
        colorbar_size = (int(75*(270/width)), int(height*(270/width)))
        background_size=(int((270*len(templates))+colorbar_size[0]), int(height*(270/width)+25))    
        background = Image.new('RGBA', background_size, (255, 0, 0, 0))
        cb = Image.open(output_dirpath+'/colorbar.png')
        cb_resized=cb.resize(colorbar_size, Image.LANCZOS)
        background.paste(cb_resized, ((270*len(templates)),0))
        out_dir = os.fsencode(output_dirpath+'/output')
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(im_name[i]):
                im = Image.open(output_dirpath+'/output/'+filename)
                im.palette = None
                resized_filename=im.resize((270, int((270/width*height))), Image.LANCZOS)
                for j in range(len(templates)):
                    if filename[:(len(filename)-4)].endswith(templates[j]+'_'+str(j)):
                        background.paste(resized_filename, ((j*270),0))
                background.save(output_dirpath+'/output/pdf/'+im_name[i]+'.png', 'PNG')
    #save all pictures from pdf folder in .pdf file
    if not os.path.exists(output_dirpath +'/output/pdf'):
        os.makedirs(output_dirpath+'/output/pdf')
    if os.path.exists(output_dirpath + '/output/pdf/whole_colormap.pdf'):
        os.remove(output_dirpath + '/output/pdf/whole_colormap.pdf')
    pdf_file = output_dirpath+'/output/pdf/whole_colormap.pdf'
    out_dir = os.fsencode(output_dirpath+'/output/pdf')
    images = []
    #font = ImageFont.truetype("courbi.ttf", 40, encoding="unic")
    font1 = ImageFont.truetype(dirpath+"/arial.ttf", 30, encoding="unic")
    files = os.listdir(out_dir)
    for file in sorted(files):
        filename0 = os.fsdecode(file)
        if filename0.endswith(".png"):
            filename1 = filename0[0:(len(filename0)-4)]          #this is the legend name which coresponds to the name in values.csv file.
            im = Image.open(output_dirpath+'/output/pdf'+'/'+filename0)
            img = Image.new('RGB', background_size, '#000000')
            img.paste(im, (0,0), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((10, ((270/width*height)-10)), filename1, fill='#FFFFFF', font=font1)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(output_dirpath + '/output/pdf/whole_colormap.pdf'):
        print ("File 'whole_colormap.pdf' saved in an 'output/pdf' folder") #show it in a message box
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print ('Something went wrong!')
    
#WHOLE_ONE_COLOR
#pick the color https://htmlcolorcodes.com/
#green by default

#iterate through the all values in the values.csv and create a numpy array with colors from corresponding colormap

def whole_one_color(color=[0, 255, 0]): #the color must be entered as list [] or string '' in RGB format
    global cv2, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont, time
    global labels_list, values_normalized, dirpath, output_dirpath, val, min_max, im_name
    
    start_time = time.time()
    
    initialization()
    create_templ(animal, templates)
    areas_viz()
    identify_events()
    to_pixel_coordinates()
    
    if ' ' in color:
        color=color.split(', ')
    if isinstance(color, str)==True:
        color=color.split(',')    
    for i in range(len(color)):
        color[i]=int(color[i])
        
    while len(color)!=3:
        print ("Wrong color format. The color must be in RGB format.")
        color = input("Enter the color in RGB format as [] or '': ")
        if ' ' in color:
            color=color.split(', ')
        if isinstance(color, str):
            color=color.split(',')
        for i in range(len(color)):
            color[i]=int(color[i])

    color.append(255)

    try:
        values=pd.read_csv(data_dirpath, index_col=0)
        print("Identified file 'values.csv': \n")
        ds=values.describe()
        ds_to_html = ds.to_html()
        html_file= open(output_dirpath+"/0_figures.html","a")
        html_file.write('<h1>Descriptive Statistics For <i>values.csv</i></h1>\n')
        html_file.write(ds_to_html+'\n')
        html_file.close()
    except(TypeError, pd.errors.ParserError):
        print('Cannot open "values.csv".')
        pass
    except(FileNotFoundError, IOError):
        print("Cannot find 'values.csv'.")
        pass
    except(pd.errors.DtypeWarning):
        print("Data types in 'values.csv' are not uniform.")
        pass
    max_col=values.max()
    max_val=max(max_col, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    min_col=values.min()
    min_val=min(min_col, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    values_normalized=(values-min_val)/(max_val-min_val)
    min_max=[min_val, max_val]
    val = [values_normalized]

    #manally create custom colorbar
    colorbar_size = (70, 270) 
    colorbar = Image.new('RGBA', colorbar_size, ((148, 151, 160, 255))) 
    colorline=Image.new('RGBA', (16, 250), (0, 0, 0, 0))
    for j in range(1,250):
        if color[3]==0:
            pass
        elif j%3==0:
            color[3]=color[3]-3
        for i in range(16):    
            colorline.putpixel((i, j), tuple(color))
            if j==1 or j==249:
                colorline.putpixel((i, j), (0,0,0,255))
                for k in range(5):
                    colorbar.putpixel((i+k+5, j+10), (0,0,0,255))
            if i==0 or i==15:
                colorline.putpixel((i, j), (0,0,0,255))

    draw1 = ImageDraw.Draw(colorbar)
    font=ImageFont.truetype(dirpath+"/arial.ttf", 20, encoding="unic")
    draw1.text((29, 5), str(min_max[1]),fill='#000000', font=font)
    draw1.text((28, 250), str(min_max[0]),fill='#000000', font=font)
    colorbar.paste(colorline, (5,10), colorline)
    colorbar.save(str(output_dirpath+'/colorbar'+'.png'), 'PNG')
    
    #variable colors holds color with corresponding trasparrency for each value from values.csv file
    colors = []
    im_name = list(val[0].index)
    for i in range(len(val)):
        colors.append([])
        shape=val[i].shape
        for row in range(shape[0]):
            colors[i].append([])
            for col in range(shape[1]):
                va = val[i].iloc[row,col]
                alpha = int(255*va)
                color[3]=alpha
                colors[i][row].append(tuple(color))
    print("Coloring templates...")
    #coloring each slice.
    def color_templ(im_name, slice_no,t):# slice_no is templates[t] from outer loop referring to the index in 'templates'
        global width, height
        identifier=str(im_name) #name is a variable from the outer loop iterating though the index column
        slice_no = str(slice_no) 
        out_dir = os.fsencode(output_dirpath+'/output') 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                label_name=identifier+'_'+slice_no+'_'+str(t)
                templ = Image.open(output_dirpath+'/output/'+slice_no+'_'+str(t)+'.png')
                width, height = templ.size
                templ1=Image.new('RGBA', (width, height), (255,255,255,0))
                for i in range(len(labels_l[t])): # t is the variable from outer loop referring to the index in 'templates'
                    for k in range(len(labels_l[t][i])): #iterating within areas for each sample (aka rows)
                        event = labels_l[t][i][k]
                        for xy in range(len(event)):
                            if event == '':
                                pass
                            else:
                                pixel_w = event[xy][0]
                                pixel_h = event[xy][1]
                                templ1.putpixel((pixel_w, pixel_h), colors[0][name][i])
                                templ1.putpixel((pixel_w-1, pixel_h-1), colors[0][name][i])
                                templ1.putpixel((pixel_w+1, pixel_h+1), colors[0][name][i])
                                templ1.putpixel((pixel_w-1, pixel_h+1), colors[0][name][i])
                                templ1.putpixel((pixel_w+1, pixel_h-1), colors[0][name][i])
                templ1 = templ1.filter(ImageFilter.GaussianBlur(radius=4))
                templ1.palette = None
                templ.paste(templ1, (0,0), templ1)
                templ.save(str(output_dirpath+'/output/'+label_name+'.png'), 'PNG')

    for name in range(len(im_name)):
        for t in range(len(templates)):
            color_templ(im_name[name], templates[t],t)      
       
    #saving .pdf
    #variable im_name is a list that holds names for all samples from the file values.csv as strings
    #width, height go from the previous function and are the width and height of the template and saved images
    if not os.path.exists(output_dirpath + '/output/pdf'):
        os.makedirs(output_dirpath + '/output/pdf')
    for i in range(len(im_name)):
        colorbar_size = (int(70*width/270), int(height*(270/width)))
        background_size=(int((270*len(templates))+colorbar_size[0]), int(height*(270/width)+25))    
        background = Image.new('RGBA', background_size, (255, 0, 0, 0))
        cb = Image.open(output_dirpath+'/colorbar.png')
        cb_resized=cb.resize(colorbar_size, Image.LANCZOS)
        background.paste(cb_resized, ((270*len(templates)),0))
        out_dir = os.fsencode(output_dirpath+'/output')
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(im_name[i]):
                im = Image.open(output_dirpath+'/output/'+filename)
                im.palette = None
                resized_filename=im.resize((270, int((270/width*height))), Image.LANCZOS)
                for j in range(len(templates)):
                    if filename[:(len(filename)-4)].endswith(templates[j]+'_'+str(j)):
                        background.paste(resized_filename, ((j*270),0))
                background.save(output_dirpath+'/output/pdf/'+im_name[i]+'.png', 'PNG')
    #save all pictures from pdf folder in .pdf file
    if not os.path.exists(output_dirpath + '/output/pdf'):
        os.makedirs(output_dirpath + '/output/pdf')
    if os.path.exists(output_dirpath + '/output/pdf/whole_one_color.pdf'):
        os.remove(output_dirpath + '/output/pdf/whole_one_color.pdf')
    pdf_file = output_dirpath + '/output/pdf/whole_one_color.pdf'
    out_dir = os.fsencode(output_dirpath + '/output/pdf')
    images = []
    font1 = ImageFont.truetype(dirpath+"/arial.ttf", 30, encoding="unic")
    files = os.listdir(out_dir)
    for file in sorted(files):
        filename0 = os.fsdecode(file)
        if filename0.endswith(".png"):
            filename1 = filename0[0:(len(filename0)-4)]          #this is the legend name which coresponds to the name in values.csv file.
            im = Image.open(output_dirpath + '/output/pdf/'+filename0)
            img = Image.new('RGB', background_size, '#000000')
            img.paste(im, (0,0), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((10, ((270/width*height)-10)), filename1, fill='#FFFFFF', font=font1)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(output_dirpath + '/output/pdf/whole_one_color.pdf'):
        print ("File 'whole_one_color.pdf' saved in an 'output/pdf' folder")
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print ('Something went wrong!')
    
#colormaps https://matplotlib.org/3.2.1/tutorials/colors/colormaps.html
#https://matplotlib.org/examples/color/colormaps_reference.html

def two_sided_colormap(colormap='viridis'):
    global cv2, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont
    global labels_list,values_normalized, dirpath, output_dirpath, val, min_max, im_name, right, left
    start_time = time.time()
    
    initialization()
    create_templ(animal, templates)
    areas_viz()
    identify_events()
    to_pixel_coordinates()
    
    open_two_sided(colormap) #open the values1.csv and values2.csv files
    
    cmap=matplotlib.cm.get_cmap(colormap)
    ax = plt.subplot(111)
    im = ax.imshow(np.array(min_max).reshape((2, 1)),cmap=cmap)
    plt.colorbar(im, ax=ax)
    ax.remove()
    plt.savefig(output_dirpath+'/colorbar.png', bbox_inches='tight')
    colors = []
    im_name = list(val[0].index)
    for i in range(len(val)):
        colors.append([])
        shape=val[i].shape
        for row in range(shape[0]):
            colors[i].append([])
            for col in range(shape[1]):
                va = val[i].iloc[row,col]
                rgba = list(cmap(va))
                for c in range(4):
                    rgba[c]=int(rgba[c]*255)
                colors[i][row].append(tuple(rgba))
    print("Coloring templates...")
    #coloring each slice and saving with name from arguments (identifier).
    def color_templ(im_name, slice_no,t):# slice_no is templates[t] from outer loop referring to the index in 'templates'
        global width, height
        identifier=str(im_name) #name is a variable from the outer loop iterating though the index column
        slice_no = str(slice_no) 
        out_dir = os.fsencode(output_dirpath+'/output') 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                label_name=identifier+'_'+slice_no+'_'+str(t)
                templ = Image.open(output_dirpath+'/output/'+slice_no+'_'+str(t)+'.png')
                width, height = templ.size
                templ1=Image.new('RGBA', (width, height), (255,255,255,0))
                for i in range(len(labels_l[t])): # t is the variable from outer loop referring to the index in 'templates'
                    for k in range(len(labels_l[t][i])): #iterating within areas for each sample (aka rows)
                        event = labels_l[t][i][k]
                        for xy in range(len(event)):
                            if event == '':
                                pass
                            else:
                                pixel_w = event[xy][0]
                                pixel_h = event[xy][1]
                                if pixel_w<int(width/2): #fill the left part with data from file values1.csv
                                    templ1.putpixel((pixel_w, pixel_h), colors[0][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h-1), colors[0][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h+1), colors[0][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h+1), colors[0][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h-1), colors[0][name][i])
                                if pixel_w>int(width/2): #fill the leftright part with data from file values1.csv
                                    templ1.putpixel((pixel_w, pixel_h), colors[1][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h-1), colors[1][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h+1), colors[1][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h+1), colors[1][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h-1), colors[1][name][i])
                templ1 = templ1.filter(ImageFilter.GaussianBlur(radius=1))
                templ1.palette = None
                templ.paste(templ1, (0,0), templ1)
                templ.save(str(output_dirpath+'/output/'+label_name+'.png'), 'PNG')

    for name in range(len(im_name)):
        for t in range(len(templates)):
            color_templ(im_name[name], templates[t],t)      
       
    #saving .pdf
    #variable im_name is a list that holds names for all samples from the file values.csv as strings
    #width, height go from the previous function and are the width and height of the template and saved images
    if not os.path.exists(output_dirpath + '/output/pdf'):
        os.makedirs(output_dirpath+'/output/pdf')
    for i in range(len(im_name)):
        colorbar_size = (int(70*(270/width)), int(height*(270/width)))
        background_size=(int((270*len(templates))+colorbar_size[0]), int(height*(270/width)+25))    
        background = Image.new('RGBA', background_size, (255, 0, 0, 0))
        cb = Image.open(output_dirpath+'/colorbar.png')
        cb_resized=cb.resize(colorbar_size, Image.LANCZOS)
        background.paste(cb_resized, ((270*len(templates)),10))
        out_dir = os.fsencode(output_dirpath+'/output')
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(im_name[i]):
                im = Image.open(output_dirpath+'/output/'+filename)
                im.palette = None
                resized_filename=im.resize((270, int((270/width*height))), Image.LANCZOS)
                for j in range(len(templates)):
                    if filename[:(len(filename)-4)].endswith(templates[j]+'_'+str(j)):
                        background.paste(resized_filename, ((j*270),15))
                background.save(output_dirpath+'/output/pdf'+im_name[i]+'.png', 'PNG')
    #save all pictures from pdf folder in .pdf file
    if not os.path.exists(output_dirpath+'/output/pdf'):
        os.makedirs(output_dirpath+'/output/pdf')
    if os.path.exists(output_dirpath+'/output/pdf/two_sided_colormap.pdf'):
        os.remove(output_dirpath+'/output/pdf/two_sided_colormap.pdf')
    pdf_file = output_dirpath+'/output/pdf/two_sided_colormap.pdf'
    if left is None:
        left = input('Enter the label for the left part (~6 characters): ')
    if right is None:
        right = input('Enter the label for the right part (~6 characters): ')
    out_dir = os.fsencode(output_dirpath+'/output/pdf')
    images = []
    font1 = ImageFont.truetype(dirpath+"/arial.ttf", 30, encoding="unic")
    files = os.listdir(out_dir)
    for file in sorted(files):
        filename0 = os.fsdecode(file)
        if filename0.endswith(".png"):
            filename1 = filename0[0:(len(filename0)-4)]          #this is the legend name which coresponds to the name in values.csv file.
            im = Image.open(output_dirpath+'/output/pdf'+'/'+filename0)
            img = Image.new('RGB', (background_size[0], background_size[1]+10), '#000000')
            img.paste(im, (0,10), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((10, ((270/width*height)-10)), filename1, fill='#FFFFFF', font=font1)
            draw.text((10, 3), left, fill='#FFFFFF', font=font1)
            draw.text((140, 3), right, fill='#FFFFFF', font=font1)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(output_dirpath+'/output/pdf/two_sided_colormap.pdf'):
        print ("File 'two_sided_colormap.pdf' saved in an 'output/pdf' folder")
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print ('Something went wrong!')
    
#TWO_SIDED_ONE_COLOR
#pick the color https://htmlcolorcodes.com/
#green by default

#iterate through the all values in the values.csv and create a numpy array with colors from corresponding colormap

def two_sided_one_color(color1=[255, 120, 0], color2=[0, 0, 255]):
    global cv2, os, Image, ImageDraw, ImageColor, ImageFilter, ImageFont
    global labels_list,values_normalized, dirpath, output_dirpath, data_dirpath, data_dirpath2, val, min_max, im_name, left, right
    start_time = time.time()
    
    initialization()
    create_templ(animal, templates)
    areas_viz()
    identify_events()
    to_pixel_coordinates()
    
    color=[color1, color2]
    for arg in range(len(color)):
        if ' ' in color[arg]:
            color[arg]=color[arg].split(', ')
        if isinstance(color[arg], str):
            color[arg]=color[arg].split(',')    
        for i in range(len(color[arg])):
            color[arg][i]=int(color[arg][i])

        while len(color[arg])!=3:
            print ("Wrong color format: "+str(color[arg])+". The color must be in RGB format.")
            color[arg] = input()
            if ' ' in color[arg]:
                color[arg]=color[arg].split(', ')
            if isinstance(color[arg], str):
                color[arg]=color[arg].split(',')
            for i in range(len(color[arg])):
                color[arg][i]=int(color[arg][i])
        color[arg].append(255) 
    #open values1.csv and values2.csv
    try:
        values1=pd.read_csv(data_dirpath, index_col=0)
        ds1=values1.describe()
        ds1_to_html = ds1.to_html()
        html_file = open(output_dirpath+"/0_figures.html","a")
        html_file.write('<h1>Descriptive Statistics For <i>values1.csv</i></h1>\n')
        html_file.write(ds1_to_html+'\n')
        html_file.close()
        print("Identified file 'values1.csv'. \n")
    except(TypeError, pd.errors.ParserError):
        print('Cannot open "values1.csv".')
        pass
    except(FileNotFoundError, IOError):
        print("Cannot find 'values1.csv'.")
        pass
    except pd.errors.DtypeWarning:
        print("Data types in 'values1.csv' are not uniform.")
        pass
    try:
        values2=pd.read_csv(data_dirpath2, index_col=0)
        ds2=values2.describe()
        ds2_to_html = ds2.to_html()
        html_file= open(output_dirpath+"/0_figures.html","a")
        html_file.write('<h1>Descriptive Statistics For <i>values2.csv</i></h1>\n')
        html_file.write(ds2_to_html+'\n')
        html_file.close()
        print("Identified file 'values2.csv'. \n")
    except(TypeError, pd.errors.ParserError):
        print('Cannot open "values2.csv".')
        pass
    except(FileNotFoundError, IOError):
        print("Cannot find 'values2.csv'.")
        pass
    except pd.errors.DtypeWarning:
        print("Data types in 'values2.csv' are not uniform.")
        pass
    max_col1=values1.max()
    max_col2=values2.max()
    min_col1=values1.min()
    min_col2=values2.min()
    max_val1=max(max_col1, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    max_val2=max(max_col2, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    min_val1=min(min_col1, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    min_val2=min(min_col2, key=lambda x: x if not isinstance(x, str) else float("-inf"))
    max_v=max([max_val1, max_val2])
    min_v=min([min_val1, min_val2])
    values1_normalized=(values1-min_v)/(max_v-min_v)
    values2_normalized=(values2-min_v)/(max_v-min_v)
    min_max=[min_v, max_v]
    val = [values1_normalized, values2_normalized]

    #manally create custom colorbars
    for p in range(2):
        colorbar_size = (70, 270) 
        colorbar = Image.new('RGBA', colorbar_size, (148, 151, 160, 255))
        colorline=Image.new('RGBA', (16, 250), (0, 0, 0, 0))
        for j in range(1,250):
            if color[p][3]==0:
                pass
            elif j%3==0:
                color[p][3]=color[p][3]-3
            for i in range(16):
                for c in range(2):
                    colorline.putpixel((i, j), tuple(color[p]))
                if j==1 or j==249:
                    colorline.putpixel((i, j), (0,0,0,255))
                    for k in range(5):
                        colorbar.putpixel((i+k+5, j+10), (0,0,0,255))
                if i==0 or i==15:
                    colorline.putpixel((i, j), (0,0,0,255))

        draw1 = ImageDraw.Draw(colorbar)
        font=ImageFont.truetype(dirpath+"/arial.ttf", 20, encoding="unic")
        draw1.text((29, 5), str(min_max[1]),fill='#000000', font=font)
        draw1.text((28, 250), str(min_max[0]),fill='#000000', font=font)
        colorbar.paste(colorline, (5,10), colorline)
        colorbar.save(str(output_dirpath+'colorbar'+str(p+1)+'.png'), 'PNG')

    #variable colors holds color with corresponding transparency for each value from values.csv file
    colors = []
    im_name = list(val[0].index)
    for i in range(len(val)):
        colors.append([])
        shape=val[i].shape
        for row in range(shape[0]):
            colors[i].append([])
            for col in range(shape[1]):
                va = val[i].iloc[row,col]
                alpha = int(255*va)
                color[i][3]=alpha
                colors[i][row].append(tuple(color[i]))
    print("Coloring templates...")
    #coloring each slice.
    def color_templ(im_name, slice_no,t):# slice_no is templates[t] from outer loop referring to the index in 'templates'
        global width, height
        identifier=str(im_name) #name is a variable from the outer loop iterating though the index column
        slice_no = str(slice_no) 
        out_dir = os.fsencode(output_dirpath+'/output') 
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(slice_no):
                label_name=identifier+'_'+slice_no+'_'+str(t)
                templ = Image.open(output_dirpath+'/output'+slice_no+'_'+str(t)+'.png')
                width, height = templ.size
                templ1=Image.new('RGBA', (width, height), (255,255,255,0))
                for i in range(len(labels_l[t])): # t is the variable from outer loop referring to the index in 'templates'
                    for k in range(len(labels_l[t][i])): #iterating within areas for each sample (aka rows)
                        event = labels_l[t][i][k]
                        for xy in range(len(event)):
                            if event == '':
                                pass
                            else:
                                pixel_w = event[xy][0]
                                pixel_h = event[xy][1]
                                if pixel_w<int(width/2): #fill the left part with data from file values1.csv
                                    templ1.putpixel((pixel_w, pixel_h), colors[0][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h-1), colors[0][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h+1), colors[0][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h+1), colors[0][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h-1), colors[0][name][i])
                                if pixel_w>int(width/2): #fill the leftright part with data from file values1.csv
                                    templ1.putpixel((pixel_w, pixel_h), colors[1][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h-1), colors[1][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h+1), colors[1][name][i])
                                    templ1.putpixel((pixel_w-1, pixel_h+1), colors[1][name][i])
                                    templ1.putpixel((pixel_w+1, pixel_h-1), colors[1][name][i])
                templ1 = templ1.filter(ImageFilter.GaussianBlur(radius=4))
                templ1.palette = None
                templ.paste(templ1, (0,0), templ1)
                templ.save(str(output_dirpath+'/output'+label_name+'.png'), 'PNG')

    for name in range(len(im_name)):
        for t in range(len(templates)):
            color_templ(im_name[name], templates[t],t)      
       
    #saving .pdf
    #variable im_name is a list that holds names for all samples from the file values.csv as strings
    #width, height go from the previous function and are the width and height of the template and saved images
    if not os.path.exists(output_dirpath+'/output/pdf'):
        os.makedirs(output_dirpath+'/output/pdf')
    for i in range(len(im_name)):
        colorbar_size = (int(75*(270/width)), int(height*(270/width)))
        if color[0]==color[1]:
            background_size=(int((270*len(templates))+colorbar_size[0]), int(height*(270/width)+25))
        else:
            background_size=(int((270*len(templates))+(colorbar_size[0]*2)), int(height*(270/width)+25))
        background = Image.new('RGBA', background_size, (255, 0, 0, 0))
        if color[0]==color[1]:
            cb = Image.open(output_dirpath+'/colorbar1.png')
            cb_resized=cb.resize(colorbar_size, Image.LANCZOS)
            background.paste(cb_resized, ((270*len(templates)),10))
        else:
            cb1 = Image.open(output_dirpath+'/colorbar1.png')
            cb1_resized=cb1.resize(colorbar_size, Image.LANCZOS)
            cb2 = Image.open(output_dirpath+'/colorbar2.png')
            cb2_resized=cb2.resize(colorbar_size, Image.LANCZOS)
            background.paste(cb1_resized, (0,10))
            background.paste(cb2_resized, ((270*len(templates)+colorbar_size[0]),10))
        out_dir = os.fsencode(output_dirpath+'/output')
        
        for file in os.listdir(out_dir):
            filename = os.fsdecode(file)
            if filename.startswith(im_name[i]):
                im = Image.open(output_dirpath+'/output'+filename)
                im.palette = None
                resized_filename=im.resize((270, int((270/width*height))), Image.LANCZOS)
                for j in range(len(templates)):
                    if filename[:(len(filename)-4)].endswith(templates[j]+'_'+str(j)):
                        if color[0]==color[1]:
                            background.paste(resized_filename, ((j*270),15))
                        else:
                            background.paste(resized_filename, (((j*270)+colorbar_size[0]),0))
                background.save(output_dirpath+'/output'+im_name[i]+'.png', 'PNG')
    #save all pictures from pdf folder in .pdf file
    if not os.path.exists(output_dirpath+'/output/pdf'):
        os.makedirs(output_dirpath+'/output/pdf')
    if os.path.exists(output_dirpath+'/output/pdf/two_sided_one_color.pdf'):
        os.remove(output_dirpath+'/output/pdf/two_sided_one_color.pdf')
    pdf_file = output_dirpath+'/output/pdf/two_sided_one_color.pdf'
    if left is None:
        left = input('Enter the label for the left part (~6 characters): ')
    if right is None:
        right = input('Enter the label for the right part (~6 characters): ')
    out_dir = os.fsencode(output_dirpath+'/output/pdf')
    images = []
    #font = ImageFont.truetype("courbi.ttf", 40, encoding="unic")
    font1 = ImageFont.truetype(dirpath+"/arial.ttf", 30, encoding="unic")
    files = os.listdir(out_dir)
    for file in sorted(files):
        filename0 = os.fsdecode(file)
        if filename0.endswith(".png"):
            filename1 = filename0[0:(len(filename0)-4)]          #this is the legend name which coresponds to the name in values.csv file.
            im = Image.open(output_dirpath+'/output/pdf'+'/'+filename0)
            img = Image.new('RGB', background_size, '#000000')
            img.paste(im, (0,0), mask=im)
            draw = ImageDraw.Draw(img)
            draw.text((10+colorbar_size[0], ((270/width*height)-10)), filename1, fill='#FFFFFF', font=font1)
            draw.text((10+colorbar_size[0], 3), left, fill='#FFFFFF', font=font1)
            draw.text((140+colorbar_size[0], 3), right, fill='#FFFFFF', font=font1)
            images.append(img)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])
    if os.path.exists(output_dirpath+'/output/pdf/two_sided_one_color.pdf'):
        print ("File 'two_sided_one_color.pdf' saved in an 'output/pdf' folder")
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print ('Something went wrong!')
        
#CREATE custom LABELS
#this function creates labels on trasparrent background using information from a file auto_input.txt or user output
#the structure for the file auto_input.txt:
#line 1: species
#line2 2: slices' numbers as shown on https://scalablebrainatlas.incf.org/index.php (the value that is displayed in parenthesis)
#each next line is the areas that should be represented on a custom label where the 3rd line will be applied to the first 
#slice (template) mentioned in the second line and so on.

                        
def create_label(color=(255, 0, 0, 255)):
    global output_dirpath
    start_time = time.time()
    
    initialization()
    create_templ(animal, templates)
    areas_viz()
    identify_events()
    to_pixel_coordinates()
    
    for t in range(len(templates)):
        slice_no=str(templates[t])
        templ = Image.open(output_dirpath+'/output/'+slice_no+'_'+str(t)+'.png')
        width, height = templ.size
        templ1=Image.new('RGBA', (width, height), (255,255,255,0))
        for i in range(len(labels_l[t])): # t is the variable from outer loop referring to the index in 'templates'
            for k in range(len(labels_l[t][i])): #iterating within areas for each sample (aka rows)
                event = labels_l[t][i][k]
                for xy in range(len(event)):
                    if event == '':
                        pass
                    else:
                        pixel_w = event[xy][0]
                        pixel_h = event[xy][1]
                        templ1.putpixel((pixel_w, pixel_h), tuple(color))
                        templ1.putpixel((pixel_w-1, pixel_h-1), tuple(color))
                        templ1.putpixel((pixel_w+1, pixel_h+1), tuple(color))
                        templ1.putpixel((pixel_w-1, pixel_h+1), tuple(color))
                        templ1.putpixel((pixel_w+1, pixel_h-1), tuple(color))
        templ1 = templ1.filter(ImageFilter.GaussianBlur(radius=1))
        templ1.save(str(output_dirpath+slice_no+'_custom_label.png'), 'PNG')
    print("--- %s seconds ---" % (time.time() - start_time))

print("Brainplot was imported successfully.")