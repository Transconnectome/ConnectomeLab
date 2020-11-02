Codes used in "Genome-Wide Polygenic Scores for Common Traits Identify Young Children with Risk for Suicides"

## Models
Model1. Base model A. Y=suicide X=sociodemographic (age, sex, high_educ, marriage, site)    
Model2. Base model B. Y=suicide X=sociodemographic + KSAD   
Model3. Y=suicide X=base model A + all 25 GPS       
Model5. Y=suicide X=base model A + phenotype(w/o KSAD)  
Model6. Y=suicide X=base model A + phenotype(w/o KSAD) + GPS    
- three suicide data(ideation passive, active and attempt) for each     

## Codes
- `main_model.py`: where main function starts & where model is defined
- `dataloader.py`: Data loading file. It chooses appropriate data for each model
- `util.py`: get command line arguments
- `main_model_para.py`: Same with `main_model.py`. just for trying other hyperparameter sets
