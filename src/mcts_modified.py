
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):

    #This is the SELECTION part of MCTS

    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    #pass
    # Hint: return leaf_node

    while not board.is_ended(state):
        if node.untried_actions:
            return expand_leaf(node, board, state)
        node = best_child(node, board, state, identity, explore_faction)
        state = board.next_state(state, node.parent_action)
    return node


def best_child(node, board, state, identity, ef):

    max_child = None
    max_win = -10
    winrate = 0
    explore = 0
    for childnode in node.child_nodes.values():
        if childnode.visits != 0:
            winrate = childnode.wins / childnode.visits
            if board.current_player(state) != identity:
                winrate = 1 - winrate
            if node.visits != 0:
                explore = sqrt(log(node.visits) / childnode.visits)
        full_rate = winrate + ef * explore
        if max_child is None or full_rate > max_win:
            max_child = childnode
            max_win = full_rate
    return max_child




def expand_leaf(node, board, state):

    #This is the EXPANSION part of MCTS

    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #pass
    # Hint: return new_node

    action = choice(node.untried_actions)
    node.untried_actions.remove(action)
    new_state = board.next_state(state, action)
    new_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(new_state))
    node.child_nodes[action] = new_node

    return new_node


def rollout(board, state):

    #This is the SIMULATION part of MCTS

    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    #pass

    while not board.is_ended(state):
        action = choice(board.legal_actions(state))
        state = board.next_state(state, action)
    return state

    '''owned_boxes = board.owned_boxes(state)
    for i in range(3):
        for j in range(3):'''

    '''while not board.is_ended(state):
        owned_boxes = board.owned_boxes(state)
        for i in range(3):
            if sum(owned_boxes.get((i, j), 0) == 1 for j in range(3)) == 2:
                state = board.next_state(state, )
    return state'''

    '''while not board.is_ended(state):
        owned_boxes = board.owned_boxes(state)
        one_score = len([v for v in owned_boxes.values() if v == 1])
        two_score = len([v for v in owned_boxes.values() if v == 2])
        check = False
        for action in board.legal_actions:
            next_state = board.next_state(state, action)
            owned_boxes = board.owned_boxes(next_state)
            one_score2 = len([v for v in owned_boxes.values() if v == 1])
            two_score2 = len([v for v in owned_boxes.values() if v == 2])
            if one_score2 > one_score or two_score2 > two_score:
                state = next_state
                check = True
        if not check:
            action = choice(board.legal_actions(state))
            state = board.next_state(state, action)
    return state'''

    def outcome(owned_boxes, game_points, board1, state1):
        if game_points is not None:
            # Try to normalize it up?  Not so sure about this code anyhow.
            red_score = game_points[1] * 9
            blue_score = game_points[2] * 9
        else:
            red_score = len([v for v in owned_boxes.values() if v == 1])
            blue_score = len([v for v in owned_boxes.values() if v == 2])
        return red_score - blue_score if board1.current_player(state1) == 1 else blue_score - red_score

    curr_state = state
    curr_action = 0

    while not board.is_ended(curr_state) and curr_action < 5:
        curr_action += 1
        best_expectation = float('-inf')
        best_move = None
        for move in board.legal_actions(curr_state):
            total_score = 0.0

            # Sample a set number of games where the target move is immediately applied.
            for r in range(5):
                rollout_state = board.next_state(curr_state, move)

                # Only play to the specified depth.
                # for i in range(MAX_DEPTH):
                #     if board.is_ended(rollout_state):
                #         break
                #     rollout_move = choice(board.legal_actions(rollout_state))
                #     rollout_state = board.next_state(rollout_state, rollout_move)
                curr_depth = 0
                while not board.is_ended(rollout_state) and curr_depth < 3:
                    rollout_move = choice(board.legal_actions(rollout_state))
                    rollout_state = board.next_state(rollout_state, rollout_move)
                    curr_depth += 1

                total_score += outcome(board.owned_boxes(rollout_state),
                                       board.points_values(rollout_state), board, curr_state)

            # expectation = float(total_score) / ROLLOUTS
            # expectation = float(total_score)

            # If the current move has a better average score, replace best_move and best_expectation
            # if expectation > best_expectation:
            if total_score > best_expectation:
                best_expectation = total_score
                # best_expectation = expectation
                best_move = move
                # if expectation == 1:
                #     break
        curr_state = board.next_state(curr_state, best_move)
        # print(curr_state)
    while not board.is_ended(curr_state):
        curr_state = board.next_state(curr_state, choice(board.legal_actions(curr_state)))

    # print("Returning curr_state!", curr_state)
    return curr_state


def backpropagate(node, won):

    #This is the BACKPROPAGATE part of MCTS

    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    Some Pseudocode from Slides:
        if node is root return
        do update states in node
        backpropagate(node.parent,score)
    """
    #pass

    if node is None:
        return
    node.wins += won
    node.visits += 1
    backpropagate(node.parent, won)

    return


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        #sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

        node = traverse_nodes(node, board, state, identity_of_bot)
        delta = rollout(board, recover_state(board, root_node, node, state))
        backpropagate(node, board.points_values(delta)[identity_of_bot])

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    return best_child(root_node, board, state, identity_of_bot, 0).parent_action


def recover_state(board, root, node, state):
    actions = []
    while node != root:
        actions.append(node.parent_action)
        node = node.parent
    for action in reversed(actions):
        state = board.next_state(state, action)
    return state