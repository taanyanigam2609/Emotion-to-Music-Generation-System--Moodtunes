import pretty_midi
import numpy as np

def extract_notes(midi_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        notes = []
        if not midi_data.instruments:
            return None
        instrument = midi_data.instruments[0] 
        for note in instrument.notes:
            notes.append(note.pitch)
        return np.array(notes)
    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def sequence_to_midi(predictions, output_file, tempo_multiplier=1.0, velocity_scale=1.0):
    midi_out = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    current_time = 0.0
    step_duration = 0.25 * (1.0 / tempo_multiplier)
    for pitch in predictions:
        vel = int(min(127, max(40, 90 * velocity_scale))) 
        safe_pitch = int(min(127, max(0, pitch)))
        note = pretty_midi.Note(velocity=vel, pitch=safe_pitch, start=current_time, end=current_time + step_duration)
        piano.notes.append(note)
        current_time += step_duration
    midi_out.instruments.append(piano)
    midi_out.write(output_file)