## **bam**bi **m**odel **m**anagement (bammm)

Estimating complex models can take time. **bammm** allows one to save estimated models and to later load them as required (without the need to re-estimate them). 

Currently it is build to only work with (generalized) linear models in python that have been esimtated using [bambi](https://github.com/bambinos/bambi) but in essence it can be used to save samples from any [PyMC](https://github.com/pymc-devs/pymc) model.

## Functionality

1. Creation and mangement of database of local models (simple JSON file)
2. Model (dependent variable, fixed and random effects) and estimation parameters (no chains, samples/chain, cores) specification.
3. Automatic build of regression equation (input to bambi) using `mm.geerate_equation()`
4. Model estimation using `mm.estimate_lmm()`
5. Saving (`mm.save_model_info()`) and updating (`mm.update_model_entry()`) of estimated model information.
6. Loading previously esimtated model (`mm.estimate_lmm()`)

## Usage
### Setup
Install using pip:
```python
pip install bammm-ozika
```
Load
```python
import bammmm as mm
```

Full example script can be found [here](https://github.com/ozika/bammm/blob/main/demo/examples.py).
### Generate your local JSON database


Before first use on a project a local database needs to be generated. Specify a path for the database:
```python
db_path = os.path.join(root_dir, "demo", "my_project", "databse_name.json")
```
Initialize database:
```python
mm.models_init(db_path)
```

### Fitting a new linear model
Load database
```python
models = json.load(open(db_path, "r"))
```

Specify linear model. The idea is to have a specific model name and a "group/family" for each model. `bammm` will create a folder (model_family) and save data of individual models in there using `pickle`.

```python
# load data that come with bambi
data = bmb.load_data("sleepstudy")

model_family = "sleepstudy" # this will be used as a folder name to host the models
model_identifier = "maximum_model"
# dependent variable
mod["lmm"]["dep_var"] = "Reaction" # Reaction time
# fixed effects
mod["lmm"]["fxeff"] = ["Days"] # longitudinal data set
# random effects
mod["lmm"]["rneff"] = ["Days|Subject"]
# build equation
mod["lmm"]["eq"] = mm.generate_equation(mod["lmm"]["dep_var"], mod["lmm"]["fxeff"], mod["lmm"]["rneff"])

```
Specify estimation parameters.
```python
# fitting information
mod["est"]["nchains"] = 2
mod["est"]["nsamples"] = 4000
mod["est"]["ncores"] = 2 # number of cores to be useds in fitting
```
Specify paths and create relevant strings.
```python
mod = mm.prepare_fit(mod, model_family, model_identifier, models_path)
# save model (it's a good idea to load/save the DB often, especially if one runs multiple models at the same time)
models[mod["name"]] = mod
mm.save_model_info(models, db_path)
```
Estimate model. This also automatically saves the data to the location specified in `models_path`
```python
mod, results, m = mm.estimate_lmm(mod, data, override=0)
mm.update_model_entry(models, mod, db_path)
```

### Load previously fitted model
It is rather simple
```python
# load database
models = json.load(open(db_path, "r"))
model_name = "sleepstudy_maximum_model_2_4000" # model estimated above
mod = models[model_name]
# load model
mod, results, m = mm.estimate_lmm(mod, [], override=0)
```



I am not saying that his is the best way to achieve model saving/loading, but it seems to work well (at least for the poor practitioner of statistics that is me).
