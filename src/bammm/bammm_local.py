import pickle as pc
import json
import os
import bambi as bmb
def models_init(path):

    models= {}
    models["template"] = {}
    #json.dump(models, open(os.path.join(root_dir, "output", "models", "ut_model_database.json"), "w"), indent=3)
    models["template"]["type"] = "" # lmm/custom
    models["template"]["est"] ={}
    models["template"]["est"]["nchains"] = ""
    models["template"]["est"]["nsamples"] = ""
    models["template"]["name"] = "template_"+str(models["template"]["est"]["nchains"])+"_"+str(models["template"]["est"]["nsamples"])
    models["template"]["lmm"] ={}
    models["template"]["lmm"]["dep_var"] = ""
    models["template"]["lmm"]["fxeff"] = [""]
    models["template"]["lmm"]["rneff"] = [""]
    models["template"]["est"]["done"] = 0
    models["template"]["location"] = ""
    with open(path, 'w', encoding='utf-8') as f:
        #json.dump(data, f, ensure_ascii=False, indent=4)
        json.dump(models, f, indent=3)

def get_template():
    model = {}
    #json.dump(models, open(os.path.join(root_dir, "output", "models", "ut_model_database.json"), "w"), indent=3)
    model["type"] = "" # lmm/custom
    model["est"] = {};
    model["est"]["nchains"] = ""
    model["est"]["nsamples"] = ""
    model["name"] = "template_"+str(model["est"]["nchains"])+"_"+str(model["est"]["nsamples"])
    model["lmm"] ={};
    model["lmm"]["dep_var"] = ""
    model["lmm"]["fxeff"] = [""]
    model["lmm"]["rneff"] = [""]
    model["est"]["done"] = 0
    model["location"] = ""
    model["model_obj"] = ""
    model["data"] = ""
    return model

def generate_equation(depvar, fxeff, rneff):
    rneff = [ '('+i+')' for i in rneff ]
    eq = depvar + ' ~ ' + ' + '.join(fxeff+rneff)
    return eq
def prepare_fit(mod, model_family, model_identifier, root_dir):
    mod["name"] = model_family + "_" + model_identifier+"_"+str(mod["est"]["nchains"])+"_"+str(mod["est"]["nsamples"])
    # specify model data location
    mod["model_folder"] = models_path
    if not(os.path.exists(mod["model_folder"])):
        os.mkdir(mod["model_folder"])
    mod["location"] = os.path.join(mod["model_folder"], mod["name"]+".dic")
    return mod

def estimate_lmm(mod, data, override=0):
    print(mod["current_sys_location"])
    if not(os.path.exists(mod["current_sys_location"])) or (override==1):
        m = bmb.Model(mod["lmm"]["eq"], data)
        if not ("ncores" in mod["est"]):
            mod["est"]["ncores"] = None #default set to max https://bambinos.github.io/bambi/main/api_reference.html
        results = m.fit(draws=mod["est"]["nsamples"], chains=mod["est"]["nchains"], cores=mod["est"]["ncores"])
        mod["est"]["done"] = 1
        pc.dump( results, open( mod["current_sys_location"], "wb+" ) )
    else:
        m = []
        print("Model "+ mod["name"] + " already exist, loading it.");
        with open( mod["current_sys_location"], "rb" ) as f:
            unpickler = pc.Unpickler(f)
            results = unpickler.load()
    return mod, results, m

def save_model_info(models, path):
    json.dump(models, open(path, "w"), indent=3)

def update_model_entry(models, mod, path):
    models = json.load(open(path, "r"))
    models[mod["name"]] = mod
    mm.save_model_info(models, path)


def remove_model_from_db(databse, names, delete_data=0):
    models = json.load(open(databse, "r"))
    for m in names:
        if m in models.keys():
            models.pop(m)
            print(models)
    json.dump(models, open(databse, "w"), indent=3)
