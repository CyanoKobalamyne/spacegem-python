import synthesizer
from synthesizer import Writer, Synthesizer, Waveform
synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
writer = Writer()
start = 130.81
mul = [0,2,4,5,7,9,11,12,14,16,17,19,21,23]
for i in range(len(mul)):
    wave = synthesizer.generate_chord([130.81*2**(mul[i]/12)], 0.5)
    writer.write_wave("./" + str(i) + ".wav", wave)
