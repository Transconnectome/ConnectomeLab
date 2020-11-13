def get_type(args):

    if args.demo and not args.ksad and not args.gps and not args.gps_sig and not args.pheno and not args.fam:
        model = 'Model1'
    elif args.demo and args.ksad and not args.gps and not args.gps_sig and not args.pheno and not args.fam:
        model = 'Model2'
    elif args.demo and not args.ksad and args.gps and not args.gps_sig and not args.pheno and not args.fam:
        model = 'Model3'
    elif args.demo and not args.ksad and not args.gps and args.gps_sig and not args.pheno and not args.fam:
        model = 'Model4'
    elif args.demo and not args.ksad and not args.gps and not args.gps_sig and args.pheno and not args.fam:
        model = 'Model5'
    elif args.demo and not args.ksad and args.gps and not args.gps_sig and args.pheno and not args.fam:
        model = 'Model6'
    elif args.demo and not args.ksad and not args.gps and args.gps_sig and args.pheno and not args.fam:
        model = 'Model7'
    elif args.demo and not args.ksad and not args.gps and not args.gps_sig and not args.pheno and args.fam:
        model = 'Model8'
    elif args.demo and not args.ksad and not args.gps and not args.gps_sig and args.pheno and args.fam:
        model = 'Model9'
    elif args.demo and not args.ksad and args.gps and not args.gps_sig and args.pheno and args.fam:
        model = 'Model10'
    elif args.demo and not args.ksad and not args.gps and args.gps_sig and args.pheno and args.fam:
        model = 'Model11'

    print(f'Model: {model}')
    
def select_model(model, data):
    args = define_args()

    if model == "Model1":
        args.set_model(t=data)
    elif model == "Model2":
        args.set_model(t=data, k=True)
    elif model == "Model3":
        args.set_model(t=data, g=True)
    elif model == "Model4":
        args.set_model(t=data, gs=True)
    elif model == "Model5":
        args.set_model(t=data, p=True, f=True)
    elif model == "Model6":
        args.set_model(t=data, g=True, p=True, f=True)
    elif model == "Model7":
        args.set_model(t=data, gs=True, p=True, f=True)
    elif model == "Model8":
        args.set_model(t=data, f=True)
    elif model == "Model9":
        args.set_model(t=data, p=True)
    elif model == "Model10":
        args.set_model(t=data, pp=True)
    elif model == "Model11":
        args.set_model(t=data, pp=True, g=True)
    elif model == "Model12":
        args.set_model(t=data, pp=True, gs=True)
    elif model == "Model13":
        args.set_model(t=data, pp=True, f=True)
    elif model == "Model14":
        args.set_model(t=data, pp=True, g=True, f=True)
    elif model == "Model15":
        args.set_model(t=data, pp=True, gs=True, f=True)
        
    return args

class define_args():
    def __init__(self):
        self.set_model(t='ideation')
    
    def set_model(self, t, d=True, k=False, g=False, gs=False, p=False, f=False, pp=False, ne=None, md=None):
        self.type = t
        self.demo = d
        self.ksad = k
        self.gps = g
        self.gps_sig = gs
        self.pheno = p
        self.fam = f
        self.pheno_p = pp
        self.ne = ne
        self.md = md