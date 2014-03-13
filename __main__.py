import math
import numpy
import scipy.io.wavfile as wav

sin = lambda f, t, sr: math.sin( 2 * math.pi * t * f / sr )

def generate_tone ( f, duration, attack, decay, release, max_volume, sustain_volume, sample_rate ):
    duration *= sample_rate
    attack *= sample_rate
    decay *= sample_rate
    release *= sample_rate
    sustain = duration - attack + decay + release

    if ( sustain < 0 ):
        raise AttributeError( "Total of attack, decay, and release values is greater than duration")

    tone = []
    d_start = attack
    s_start = d_start + decay
    r_start = s_start + sustain

    s_drop_factor = 1.0 - sustain_volume / max_volume

    for t in numpy.arange( attack ):
        tone.append( sin( f, t, sample_rate ) * max_volume * t / attack )

    for t in numpy.arange( decay ):
        tone.append( sin( f, d_start + t, sample_rate ) * max_volume * ( 1 - s_drop_factor * t / decay ) )

    for t in numpy.arange( sustain ):
        tone.append( sin( f, s_start + t, sample_rate ) * sustain_volume )

    for t in numpy.arange( release ):
        tone.append( sin( f, r_start + t, sample_rate ) * sustain_volume * ( 1 - t / release ) )

    return tone

# print generate_tone( 440, 4000, 4000, 60000, 10000, 6000, 4000 )

wav.write( "sin_original.wav", 44100, numpy.array( generate_tone( 220, 0.2, 0.2, 0.5, 0.2, 6000, 2000, 44100 ) + generate_tone( 440, 0.2, 0.2, 0.5, 0.2, 6000, 2000, 44100 ) + generate_tone( 880, 0.2, 0.2, 0.5, 0.2, 6000, 2000, 44100 ) + generate_tone( 1760, 0.2 , 0.2, 0.5, 0.2, 6000, 2000, 44100 ), dtype=numpy.int16 ) )
