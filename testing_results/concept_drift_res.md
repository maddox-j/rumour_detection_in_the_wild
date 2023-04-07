Twitter15 Base
Total_Test_Accuracy: 0.8937|NR F1: 0.8510|FR F1: 0.8604|TR F1: 0.9502|UR F1: 0.9132

Twitter16 Base
Total_Test_Accuracy: 0.8824|NR F1: 0.8793|FR F1: 0.8888|TR F1: 0.9117|UR F1: 0.8431

# 5 Fold Cross Validation

Simulate what would happen if you were to evaluate the train mdoel on a different dataset.
We  can't evaluate it on it's own dataset again as the splits are random; training data may now appear in the validation set and inflate the result.

Twitter15 Weights on Twitter16

Total_Test_Accuracy: 0.2502|NR F1: 0.3635|FR F1: 0.1812|TR F1: 0.1844|UR F1: 0.1569

Twitter16Weights on Twitter15

Total_Test_Accuracy: 0.2798|NR F1: 0.3637|FR F1: 0.2863|TR F1: 0.1169|UR F1: 0.2151