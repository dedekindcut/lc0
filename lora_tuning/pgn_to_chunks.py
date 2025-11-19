import chess
import chess.pgn
import lczero.backends as lczero
import numpy as np
import struct
import gzip
import os
import argparse
import sys

# V6 Structure from chunkparser.py
# V6_STRUCT_STRING = '4si7432s832sBBBBBBBbfffffffffffffffIHH4H'
V6_STRUCT = struct.Struct('4si7432s832sBBBBBBBbfffffffffffffffIHH4H')
V6_VERSION = struct.pack('i', 6)

def get_input_planes(game_state, backend):
    """
    Extracts 104 bitplanes from Lc0 backend Input.
    Returns bytes (832 bytes).
    """
    inp = game_state.as_input(backend)
    planes = []
    # Lc0 usually has 112 planes. V6 stores 104 compressed planes.
    # The first 104 planes are usually history planes (13 * 8).
    for i in range(104):
        mask = inp.mask(i)
        # Convert u64 to bytes (little endian)
        planes.append(struct.pack('<Q', mask))
    return b''.join(planes)

def parse_pgn_file(pgn_path, backend, output_path):
    print(f"Processing {pgn_path} -> {output_path}")
    
    pgn = open(pgn_path)
    
    with gzip.open(output_path, 'wb') as out:
        # Write header? chunkparser expects file to start with version
        # single_file_gen reads version (4 bytes) then records.
        # out.write(V6_VERSION) # NO! The record itself starts with version.
        
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            
            game_count += 1
            board = game.board()
            
            # Result
            result_str = game.headers.get("Result", "*")
            if result_str == "1-0":
                result_q = 1.0
                result_d = 0.0 # assuming no draw
            elif result_str == "0-1":
                result_q = -1.0
                result_d = 0.0
            elif result_str == "1/2-1/2":
                result_q = 0.0
                result_d = 1.0
            else:
                continue # Skip unknown result
                
            # Moves
            moves = list(game.mainline_moves())
            
            # FEN
            root_fen = game.headers.get("FEN")
            if game.headers.get("SetUp") != "1":
                root_fen = None # Startpos
            
            # Replay
            # We need to build history for Lc0.
            # lczero.backends.GameState takes history.
            # But constructor takes `moves` list.
            
            # Iterate positions
            # We need full move history for each position?
            # GameState(fen, moves)
            
            # Optimization: Lc0 GameState might not need full history if we just want current position planes?
            # But Lc0 input includes history.
            # We should pass the moves played so far.
            
            move_strs = []
            board.reset()
            
            # Parse evals from comments?
            # Comment format: {+0.55/6 0.257s}
            # We need Policy (Pi) and Q/D/M.
            # If we don't have detailed policy in PGN, we can't train policy unless we use the move played as 1.0 (one-hot).
            # PGN comments usually only have best move score.
            # Actually the user said "piece odds games ... vs various human like opponents".
            # Usually we want to learn from the *winner* or improve *policy* to match the game?
            # If we assume the games are good, we train policy = played move.
            
            node = game
            
            # Start form initial position
            board = game.board()
            
            while node.next():
                next_node = node.next()
                move = next_node.move
                
                # Current position (before move)
                # We want to generate training data for THIS position.
                
                # Create Lc0 GameState
                # We need moves list to reconstruct history
                # Converting all moves to strings might be slow, but necessary for GameState constructor
                
                # Optimization: GameState might handle incrementally? No, python binding creates new GameState.
                
                # We need FEN? No, just moves from start.
                # If standard start:
                gs = lczero.GameState(fen=root_fen, moves=move_strs)
                
                # Get Input
                # We need a dummy backend to generate input?
                # backend.evaluate is not needed, just as_input.
                
                # Planes
                planes_bytes = get_input_planes(gs, backend)
                
                # Policy
                # One-hot encoding of the played move
                # We need to know the index of 'move' in Lc0 output.
                # lczero-bindings doesn't seem to expose Move -> Index directly easily?
                # `game_state.policy_indices()` might give indices of legal moves? No.
                # `backend_caps`? 
                
                # We can use `lc0_az_policy_map` or similar if we know the format.
                # `dataset.py` uses standard mapping.
                # We need to map `chess.Move` to index 0..1857.
                
                # Let's implement `encode_move(move, board)`
                # Using `lc0_az_policy_map` logic (already imported in model.py, let's reuse or reimplement)
                
                # Probs array
                probs = [0.0] * 1858
                
                # Calculate move index
                # We need to handle mirroring if black to move?
                # Lc0 input planes are always "side to move".
                # Policy output is also relative?
                # Yes, "All moves decoded are from the point of view of the side after the move..."
                # Wait, policy is usually relative to side to move.
                
                # Use `policy_index` module from `lora_tuning`.
                # I need to verify how to map.
                # Usually: tensor index = move index.
                
                move_uci = move.uci()
                # Flip move if black?
                # Lc0 policy map usually expects White-relative coordinates if input is White-relative?
                # Or if input is canonical (always "us"), then move is "us".
                # Python-chess moves are absolute (e.g. a7a5).
                # If black to move, we need to flip the move for the policy map?
                # Yes, if using canonical input.
                
                us = board.turn
                if us == chess.BLACK:
                    # Flip move
                    # a1 <-> a8, etc.
                    # mirrors rank.
                    # chess.Move.uci() returns 'e7e5'
                    # we need to flip ranks: e7->e2, e5->e4
                    
                    def flip_square(sq):
                        return sq ^ 56
                    
                    move_to_encode = chess.Move(flip_square(move.from_square), flip_square(move.to_square), move.promotion)
                else:
                    move_to_encode = move
                    
                # Policy Index
                # Need to map `move_to_encode` (uci) to index.
                # I can use `policy_index.py` from lczero-training.
                
                try:
                    # Need to import policy_index
                    import policy_index
                    idx = policy_index.policy_index.index(move_to_encode.uci())
                    probs[idx] = 1.0
                except ValueError:
                    # Move not in policy map? (e.g. underpromotion?)
                    pass
                
                # Input format
                # Get from backend capabilities
                if args.input_format >= 0:
                    input_format = args.input_format
                else:
                    input_format = backend.capabilities().input_format()
                
                # Castling rights (from board)
                # We need to encode them.
                # Lc0 V6 expects: us_ooo, us_oo, them_ooo, them_oo (uint8)
                # V6 planes usually do NOT include castling planes if they are passed separately?
                # Chunkparser adds them back.
                # So we just set the bytes.
                
                us_ooo = 1 if board.has_queenside_castling_rights(us) else 0
                us_oo = 1 if board.has_kingside_castling_rights(us) else 0
                them_ooo = 1 if board.has_queenside_castling_rights(not us) else 0
                them_oo = 1 if board.has_kingside_castling_rights(not us) else 0
                
                # STM / EnPassant
                # Chunkparser: side_to_move_or_enpassant
                # If canonical, it is EP file (or 0 if none) + STM bit in invariance?
                # Actually for InputFormat 5:
                # data.side_to_move_or_enpassant = position.GetBoard().en_passant().as_int() >> 56;
                # i.e. the file index of EP square (0-7) or something?
                # Or bitmask?
                
                ep = 0
                if board.ep_square:
                    # File of EP square
                    ep_file = chess.square_file(board.ep_square)
                    # We need to flip if Black?
                    # The EP square rank is 2 or 5.
                    # If we flipped the board, EP rank is always 5 (for them) or 2 (for us)?
                    # Canonical means "Us" is always White perspective.
                    # EP is only possible if pawn moved double.
                    # It seems Lc0 stores EP as a bitmask of files?
                    ep = (1 << ep_file)
                
                # Rule 50
                rule50 = board.halfmove_clock
                
                # Invariance Info
                # "Send transform in deprecated move count"
                # We assume identity transform (0).
                # Bit 7: side to move (input type 3+).
                # If we canonicalized (which GameState does), do we set STM?
                # Usually canonical means STM is always "White" in input planes.
                # But we need to record if it was Black for reversibility?
                invariance_info = 0
                if us == chess.BLACK:
                    invariance_info |= (1 << 7)
                    
                # Q, D, M
                # We can use result_q for everything if we don't have search data
                # Or parse comment
                root_q = result_q # From game result
                best_q = result_q
                root_d = result_d
                best_d = result_d
                root_m = 0.0
                best_m = 0.0
                plies_left = 0.0 # Unknown
                
                # Played Q/D/M
                played_q = result_q
                played_d = result_d
                played_m = 0.0
                
                # Indices
                played_idx = idx
                best_idx = idx
                
                # Pack
                # 4si7432s832sBBBBBBBbfffffffffffffffIHH4H
                # 4s: version (V6)
                # i: input format (5)
                # 7432s: probs (1858 floats) -> convert to bytes
                probs_bytes = np.array(probs, dtype=np.float32).tobytes()
                
                # Pack
                record = V6_STRUCT.pack(
                    V6_VERSION,
                    input_format,
                    probs_bytes,
                    planes_bytes,
                    us_ooo, us_oo, them_ooo, them_oo,
                    ep,
                    rule50,
                    invariance_info,
                    0, # dep_result
                    root_q, best_q, root_d, best_d, root_m, best_m, plies_left,
                    result_q, result_d,
                    played_q, played_d, played_m,
                    0.0, 0.0, 0.0, # orig q,d,m (NaN or 0)
                    1, # visits
                    played_idx, best_idx,
                    0, 0, 0, 0 # reserved
                )
                
                out.write(record)
                
                # Advance
                node = next_node
                move_strs.append(move.uci())
                board.push(move)
                
        print(f"Processed {game_count} games.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input PGN")
    parser.add_argument("--output", required=True, help="Output .gz chunk")
    parser.add_argument("--weights", required=True, help="Weights for backend")
    parser.add_argument("--input-format", type=int, default=-1, help="Force input format (1=Classical, 5=CanonicalV2)")
    args = parser.parse_args()
    
    # Init backend
    weights = lczero.Weights(args.weights)
    backend = lczero.Backend(weights=weights, backend="eigen")
    
    parse_pgn_file(args.input, backend, args.output)
