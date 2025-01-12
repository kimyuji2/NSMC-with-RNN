#%% 
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import re
#%% 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class NSMC_classifier(nn.Module):
    def __init__(self, num_vocab, embedding_dim, hidden_dim, num_layers, out_node, drop_percent=0.2, model="RNN"):  # RNN LSTM GRU를 모두 쓰기 위해서 넣은 option이다. RNN을 default로 넣음
        super(NSMC_classifier, self).__init__()
        # 변수 다 설정
        self.model = model
        self.num_vocab = num_vocab
        # embedding layer: embedding_dim 맞추기
        self.embed = nn.Embedding(num_embeddings=num_vocab, embedding_dim=embedding_dim)
        self.rnn = nn.RNN(input_size=embedding_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
        self.gru = nn.GRU(input_size=embedding_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
        self.dropout = nn.Dropout(drop_percent)

        self.fc = nn.Linear(hidden_dim, out_node) # binary이기 때문에 out_node = 1 (sigmoid를 통해 0,1사이 값 출력)
        self.sigmoid = nn.Sigmoid()


    def forward(self, x):
        x = self.embed(x)

    # 원하는 모델 골라쓰기!
        if self.model == "RNN":
            out, hidden = self.rnn(x)
        elif self.model == "LSTM":
            out, (hidden, cell_state) = self.lstm(x)
            out = self.dropout(out)
        elif self.model == "GRU":
            out, hidden = self.gru(x)
        else:
            print("choose a model in ['RNN', 'LSTM', 'GRU']")
            raise # 에러 발생시킴

        out = self.dropout(out)
        out = self.fc(out[:,-1,:]) # 마지막것만
        out = self.sigmoid(out)
        return out