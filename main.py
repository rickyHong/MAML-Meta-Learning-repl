import argparse
import ipdb

from maml import MAML


def argsparser():
    parser = argparse.ArgumentParser("Tensorflow Implementation of MAML")
    # Dataset
    parser.add_argument('--dataset', help='environment ID', choices=['sin'],
                        required=True)
    # MAML
    parser.add_argument('--K', type=int, default=10)
    parser.add_argument('--model_type', type=str, default='fc')
    parser.add_argument('--loss_type', type=str, default='MSE')
    # Train
    parser.add_argument('--max_steps', type=int, default=7e4)
    parser.add_argument('--alpha', type=float, default=1e-3)
    parser.add_argument('--beta', type=float, default=1e-3)
    parser.add_argument('--batch_size', type=int, default=25)
    # Test
    parser.add_argument('--test_sample', type=int, default=100)
    args = parser.parse_args()
    return args


def get_dataset(dataset_name, K_shots):
    if dataset_name == 'sin':
        from dataset.SinDataGenerator import dataset
    else:
        ValueError("Invalid dataset")
    return dataset(K_shots)


def main(args):
    dataset = get_dataset(args.dataset, args.K)
    finn = MAML(dataset,
                args.model_type,
                args.loss_type,
                dataset.dim_input,
                dataset.dim_output,
                args.alpha,
                args.beta,
                args.K,
                args.batch_size
                )
    finn.learn(args.batch_size, dataset, args.max_steps)
    finn.test(dataset, args.test_sample)

if __name__ == '__main__':
    args = argsparser()
    main(args)