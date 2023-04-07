# Ablation Study on Model

Baselines 

Twitter15 Base
Total_Test_Accuracy: 0.8937|NR F1: 0.8510|FR F1: 0.8604|TR F1: 0.9502|UR F1: 0.9132

Twitter16 Base
Total_Test_Accuracy: 0.8824|NR F1: 0.8793|FR F1: 0.8888|TR F1: 0.9117|UR F1: 0.8431

## Removing textual features
- We removed the vec features from the tree and replaced every single on with "0:1".

Twitter15

Total_Test_Accuracy: 0.7175|NR F1: 0.7399|FR F1: 0.7444|TR F1: 0.7301|UR F1: 0.6286 - 0.5

Total_Test_Accuracy: 0.6539|NR F1: 0.6272|FR F1: 0.6977|TR F1: 0.6385|UR F1: 0.6133 - 0.7

Total_Test_Accuracy: 0.4608|NR F1: 0.5311|FR F1: 0.4168|TR F1: 0.4400|UR F1: 0.3938 - 0.9

Total_Test_Accuracy: 0.3330|NR F1: 0.4486|FR F1: 0.0805|TR F1: 0.0000|UR F1: 0.3904 - 1.0

Twitter16
Total_Test_Accuracy: 0.7103|NR F1: 0.7064|FR F1: 0.6004|TR F1: 0.7956|UR F1: 0.7335 - 0.5

Total_Test_Accuracy: 0.6059|NR F1: 0.5633|FR F1: 0.5061|TR F1: 0.6615|UR F1: 0.6225 - 0.7

Total_Test_Accuracy: 0.4532|NR F1: 0.5228|FR F1: 0.0947|TR F1: 0.5865|UR F1: 0.3114 - 0.9

Total_Test_Accuracy: 0.3448|NR F1: 0.4760|FR F1: 0.0000|TR F1: 0.2909|UR F1: 0.0425 - 0.1

## Remove certain edges randomly.
Twitter15
### 0.5
Total_Test_Accuracy: 0.8665|NR F1: 0.8399|FR F1: 0.8723|TR F1: 0.9045|UR F1: 0.8167

Total_Test_Accuracy: 0.8712|NR F1: 0.8584|FR F1: 0.8684|TR F1: 0.9213|UR F1: 0.8376

Total_Test_Accuracy: 0.8628|NR F1: 0.8493|FR F1: 0.8644|TR F1: 0.9034|UR F1: 0.8330

Total_Test_Accuracy: 0.8610|NR F1: 0.8483|FR F1: 0.8631|TR F1: 0.9002|UR F1: 0.8282

Total_Test_Accuracy: 0.8748|NR F1: 0.8554|FR F1: 0.8820|TR F1: 0.9024|UR F1: 0.8557

### - 0.7
Total_Test_Accuracy: 0.8851|NR F1: 0.8713|FR F1: 0.8952|TR F1: 0.9161|UR F1: 0.7888

Total_Test_Accuracy: 0.8839|NR F1: 0.8592|FR F1: 0.8232|TR F1: 0.9255|UR F1: 0.8615

Total_Test_Accuracy: 0.8808|NR F1: 0.8008|FR F1: 0.8728|TR F1: 0.9094|UR F1: 0.8604

Total_Test_Accuracy: 0.8668|NR F1: 0.8482|FR F1: 0.8555|TR F1: 0.9140|UR F1: 0.7854

Total_Test_Accuracy: 0.8799|NR F1: 0.8738|FR F1: 0.8706|TR F1: 0.8407|UR F1: 0.7980

### 0.9
Total_Test_Accuracy: 0.8169|NR F1: 0.7867|FR F1: 0.8254|TR F1: 0.8616|UR F1: 0.7935

Total_Test_Accuracy: 0.8135|NR F1: 0.7825|FR F1: 0.8292|TR F1: 0.8310|UR F1: 0.8202

Total_Test_Accuracy: 0.8151|NR F1: 0.7902|FR F1: 0.8358|TR F1: 0.8389|UR F1: 0.7858

Total_Test_Accuracy: 0.8046|NR F1: 0.7875|FR F1: 0.8057|TR F1: 0.8422|UR F1: 0.7861

Total_Test_Accuracy: 0.7953|NR F1: 0.7681|FR F1: 0.8257|TR F1: 0.8396|UR F1: 0.7456
### 0.999
Total_Test_Accuracy: 0.3606|NR F1: 0.3644|FR F1: 0.3394|TR F1: 0.0000|UR F1: 0.0000

Total_Test_Accuracy: 0.5413|NR F1: 0.5543|FR F1: 0.3333|TR F1: 0.5933|UR F1: 0.0000

Total_Test_Accuracy: 0.2961|NR F1: 0.4136|FR F1: 0.0000|TR F1: 0.2689|UR F1: 0.1000

Total_Test_Accuracy: 0.2527|NR F1: 0.2697|FR F1: 0.2489|TR F1: 0.0000|UR F1: 0.2000

Total_Test_Accuracy: 0.4809|NR F1: 0.4654|FR F1: 0.3000|TR F1: 0.5800|UR F1: 0.0000

Twitter16
### 0.5
Total_Test_Accuracy: 0.8973|NR F1: 0.8602|FR F1: 0.8865|TR F1: 0.9403|UR F1: 0.9064 

Total_Test_Accuracy: 0.8845|NR F1: 0.8470|FR F1: 0.8567|TR F1: 0.9462|UR F1: 0.8740

Total_Test_Accuracy: 0.8719|NR F1: 0.8100|FR F1: 0.8327|TR F1: 0.9431|UR F1: 0.8848

Total_Test_Accuracy: 0.8797|NR F1: 0.8265|FR F1: 0.8621|TR F1: 0.9511|UR F1: 0.8809

Total_Test_Accuracy: 0.8835|NR F1: 0.8329|FR F1: 0.8657|TR F1: 0.9401|UR F1: 0.8998

### 0.7
Total_Test_Accuracy: 0.9074|NR F1: 0.7865|FR F1: 0.7607|TR F1: 0.9502|UR F1: 0.9228 

Total_Test_Accuracy: 0.8886|NR F1: 0.8161|FR F1: 0.8710|TR F1: 0.9312|UR F1: 0.9251

Total_Test_Accuracy: 0.9001|NR F1: 0.8652|FR F1: 0.8725|TR F1: 0.9365|UR F1: 0.9298

Total_Test_Accuracy: 0.8988|NR F1: 0.7620|FR F1: 0.8787|TR F1: 0.8538|UR F1: 0.9083

Total_Test_Accuracy: 0.8812|NR F1: 0.8287|FR F1: 0.8562|TR F1: 0.9252|UR F1: 0.8930

### 0.9
Total_Test_Accuracy: 0.7678|NR F1: 0.7291|FR F1: 0.7329|TR F1: 0.8112|UR F1: 0.8146 - 0.9

Total_Test_Accuracy: 0.8004|NR F1: 0.7654|FR F1: 0.7566|TR F1: 0.8582|UR F1: 0.8452

Total_Test_Accuracy: 0.8031|NR F1: 0.7697|FR F1: 0.7753|TR F1: 0.8771|UR F1: 0.8060

Total_Test_Accuracy: 0.7813|NR F1: 0.7348|FR F1: 0.7524|TR F1: 0.8767|UR F1: 0.7946

Total_Test_Accuracy: 0.7954|NR F1: 0.7613|FR F1: 0.7726|TR F1: 0.8829|UR F1: 0.7892

### 0.999
Total_Test_Accuracy: 0.1883|NR F1: 0.2714|FR F1: 0.0800|TR F1: 0.0000|UR F1: 0.0000 - 0.999

Total_Test_Accuracy: 0.1300|NR F1: 0.1333|FR F1: 0.0000|TR F1: 0.1667|UR F1: 0.0000

Total_Test_Accuracy: 0.6267|NR F1: 0.6333|FR F1: 0.1333|TR F1: 0.4000|UR F1: 0.1000

Total_Test_Accuracy: 0.4500|NR F1: 0.5467|FR F1: 0.0000|TR F1: 0.0000|UR F1: 0.0000

Total_Test_Accuracy: 0.4900|NR F1: 0.2000|FR F1: 0.0000|TR F1: 0.3333|UR F1: 0.2381