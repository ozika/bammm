import os
from groo.groo import get_root
root_dir = get_root(".root_dir_covid")
import sys
sys.path.append(os.path.join(root_dir, "covid-fear", "scripts"))
import cov_model_management as mm
import bambi as bmb
import json

## Specify which model database will be used
db_path = os.path.join(root_dir, "output", "dev", "model_management", "databse_name.json")
# initialize a database if it doesn't exist
# stored as models = {} in a JSON file
if not(os.path.exists(db_path)):
    mm.models_init(db_path)

##### Use case 1: Fitting a new model #####
# load sleepstudy set from bambi (see https://github.com/bambinos/bambi/blob/main/bambi/data/datasets.py)
data = bmb.load_data("sleepstudy")
data

# load database
models = json.load(open(db_path, "r"))

# initialize a model from a template (use during first initiation only)
mod = mm.get_template()

### specify model
model_family = "sleepstudy" # this will be used as a folder name to host the models
model_identifier = "maximum_model"
mod["type"] = "lmm" # this is more for future if we decide to add other than linear models
# dependent variable
mod["lmm"]["dep_var"] = "Reaction" # RT
# fixed effects
mod["lmm"]["fxeff"] = ["Days"]
# random effects
mod["lmm"]["rneff"] = ["Days|Subject"]
# build equation
mod["lmm"]["eq"] = mm.generate_equation(mod["lmm"]["dep_var"], mod["lmm"]["fxeff"], mod["lmm"]["rneff"])

# fitting information
mod["est"]["nchains"] = 2
mod["est"]["nsamples"] = 4000
mod["est"]["ncores"] = 2 # number of cores to be useds in fitting
mod["name"] = model_family + "_" + model_identifier+"_"+str(mod["est"]["nchains"])+"_"+str(mod["est"]["nsamples"])

# specify model data location
mod["model_folder"] = os.path.join(root_dir, "output", "dev", "model_management", "models", model_family )
if not(os.path.exists(mod["model_folder"])):
    os.mkdir(mod["model_folder"])
mod["location"] = os.path.join(mod["model_folder"], mod["name"]+".dic")

# It's usually a good idea to save the model info here
models[mod["name"]] = mod
mm.save_model_info(models, db_path)


### Fit or load model
# mod - information
# results  - samples estimated by bambi/pymc, in xarray format
# m - model object
mod, results, m = mm.estimate_lmm(mod, data, override=0)

# update the entry in models json (better use update in case more than one processes are trying to edit the json)
mm.update_model_entry(models, mod, db_path)


### Use case 2: Load a fitted model #####
models = json.load(open(db_path, "r"))
model_name = "sleepstudy_maximum_model_2_4000"
mod = models[model_name]
# load model
mod, results, m = mm.estimate_lmm(mod, [], override=0)


### Additional tools
# remove model from a database
# names need to be a list (even if it's just one model)
mm.remove_model_from_db(db_path, names)
