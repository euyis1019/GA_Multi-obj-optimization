import torchaudio
import torchaudio.compliance.kaldi as kaldi
from ais_bench.infer.interface import InferSession
import numpy as np


class WeNetASR:
    def __init__(self, model_path, vocab_path):
        """初始化模型，加载词表"""
        self.vocabulary = load_vocab(vocab_path)
        self.model = InferSession(0, model_path)
        # 获取模型输入特征的最大长度
        self.max_len = self.model.get_inputs()[0].shape[1]

    def transcribe(self, wav_file):
        """执行模型推理，将录音文件转为文本。"""
        feats_pad, feats_lengths = self.preprocess(wav_file)
        ##这里获得了特征响亮、时序信息
        output = self.model.infer([feats_pad, feats_lengths])
        #这个ais库不知道啥来头
        txt = self.post_process(output)
        return txt

    def preprocess(self, wav_file):
        """数据预处理"""
        waveform, sample_rate = torchaudio.load(wav_file)
        # 音频重采样，采样率16000
        waveform, sample_rate = resample(waveform, sample_rate, resample_rate=16000)
        # 计算fbank特征
        feature = compute_fbank(waveform, sample_rate)
        feats_lengths = np.array([feature.shape[0]]).astype(np.int32)
        # 对输入特征进行padding，使符合模型输入尺寸
        feats_pad = pad_sequence(feature,
                                 batch_first=True,
                                 padding_value=0,
                                 max_len=self.max_len)
        feats_pad = feats_pad.numpy().astype(np.float32)
        return feats_pad, feats_lengths

    def post_process(self, output):
        """对模型推理结果进行后处理，根据贪心策略选择概率最大的token，去除重复字符和空白字符，得到最终文本。"""
        encoder_out_lens, probs_idx = output[1], output[4]
        token_idx_list = probs_idx[0, :, 0][:encoder_out_lens[0]]
        token_idx_list = remove_duplicates_and_blank(token_idx_list)
        text = ''.join(self.vocabulary[token_idx_list])
        return text


def remove_duplicates_and_blank(token_idx_list):
    """去除重复字符和空白字符"""
    res = []
    cur = 0
    BLANK_ID = 0
    while cur < len(token_idx_list):
        if token_idx_list[cur] != BLANK_ID:
            res.append(token_idx_list[cur])
        prev = cur
        while cur < len(token_idx_list) and token_idx_list[cur] == token_idx_list[prev]:
            cur += 1
    return res


def pad_sequence(seq_feature, batch_first=True, padding_value=0, max_len=966):
    """对输入特征进行padding，使符合模型输入尺寸"""
    feature_shape = seq_feature.shape
    feat_len = feature_shape[0]
    if feat_len > max_len:
        # 如果输入特征长度大于模型输入尺寸，则截断
        seq_feature = seq_feature[:max_len].unsqueeze(0)
        return seq_feature

    batch_size = 1
    trailing_dims = feature_shape[1:]
    if batch_first:
        out_dims = (batch_size, max_len) + trailing_dims
    else:
        out_dims = (max_len, batch_size) + trailing_dims

    out_tensor = seq_feature.data.new(*out_dims).fill_(padding_value)
    if batch_first:
        out_tensor[0, :feat_len, ...] = seq_feature
    else:
        out_tensor[:feat_len, 0, ...] = seq_feature
    return out_tensor


def resample(waveform, sample_rate, resample_rate=16000):
    """音频重采样"""
    waveform = torchaudio.transforms.Resample(
        orig_freq=sample_rate, new_freq=resample_rate)(waveform)
    return waveform, resample_rate


def compute_fbank(waveform,
                  sample_rate,
                  num_mel_bins=80,
                  frame_length=25,
                  frame_shift=10,
                  dither=0.0):
    """提取filter bank音频特征"""
    AMPLIFY_FACTOR = 1 << 15
    waveform = waveform * AMPLIFY_FACTOR
    mat = kaldi.fbank(waveform,
                      num_mel_bins=num_mel_bins,
                      frame_length=frame_length,
                      frame_shift=frame_shift,
                      dither=dither,
                      energy_floor=0.0,
                      sample_frequency=sample_rate)
    return mat


def load_vocab(txt_path):
    """加载词表"""
    vocabulary = []
    LEN_OF_VALID_FORMAT = 2
    with open(txt_path, 'r') as fin:
        for line in fin:
            arr = line.strip().split()
            # 词表格式：token id
            if len(arr) != LEN_OF_VALID_FORMAT:
                raise ValueError(f"Invalid line: {line}. Expect format: token id")
            vocabulary.append(arr[0])
    return np.array(vocabulary)


def main():
    model_path = "offline_encoder.om"
    vocab_path = 'vocab.txt'

    model = WeNetASR(model_path, vocab_path)
    wav_file = 'sample.wav'

    txt = model.transcribe(wav_file)
    print(txt)


if __name__ == '__main__':
    main()