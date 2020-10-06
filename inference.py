import torch
import PIL
import numpy as np

def process_image(image):    
    img=PIL.Image.open(image)
    w,h = img.size
    if(w<h):
        new_w = 256
        ratio = float(new_w) / float(w)
        new_h = int(float(h) * float(ratio))
    else:
        new_h = 256
        ratio = float(new_h) / float(h)
        new_w = int(float(w) * float(ratio))
    img = img.resize((new_w , new_h), PIL.Image.ANTIALIAS)
    left = (new_w - 224)/2
    top = (new_h - 224)/2
    right = (new_w + 224)/2
    bottom = (new_h + 224)/2
    img = img.crop((left, top, right, bottom))
    np_image = np.array(img)
    np_image =np_image /255.0
    means = [0.485,0.456,0.406]
    sd = [0.229,0.224,0.225]
    np_image = np_image - means
    np_image = np_image / sd
    np_image_final = np_image.transpose((2,0,1))
    return np_image_final



def predict(image_path):
    img = process_image(image_path)   
    img = torch.from_numpy(img)
    img.unsqueeze_(0)
    img = img.float()
    with torch.no_grad():
        model.eval()
        logps = model(img)
        ps = torch.exp(logps)
        top_p,top_index = ps.topk(2 , dim=1)        

        
        #top_p=top_p.cpu().numpy()[0]
        top_p=top_p.numpy()[0]
        top_p /= sum(top_p)
          
        #top_index=top_index.cpu().numpy()[0]
        top_index=top_index.numpy()[0]
        
        
        classes = ['benign', 'malignant']
        return classes[top_index[0]], str(round(top_p[0]*100.0,2)) + '%'