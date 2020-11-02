import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Suicide Prediction Using Gradient Boosting Classifier', 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--type', type=str, default='idP', choices=['idP', 'idA', 'att'], help='Suicide data type', dest='type')
    parser.add_argument('-d', '--demographic', type=bool, default=True, help='Demographic data', dest='demo')
    parser.add_argument('-k', '--kdads', type=bool, default=False, help='Demographic data', dest='ksad')
    parser.add_argument('-g', '--gps25', type=bool, default=False, help='All GPS', dest='gps')
    parser.add_argument('-gs', '--gpssig', type=bool, default=False, help='GPS only significant', dest='gps_sig')
    parser.add_argument('-p', '--phenotype', type=bool, default=False, help='Using all of the phenotype except KSAD', dest='pheno')

    return parser.parse_args()
