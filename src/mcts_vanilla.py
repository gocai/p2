
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

    while node is not None:
        if len(node.untried_actions) != 0:
            return expand_leaf(node, board, state)
        else:
            node = best_child(node)

    return node


def best_child(node):
    bc = {}
    for x in node.child_nodes:
        #if x.visits != 0 and node.visits != 0:
        bc[x] = x.wins / (x.visits + 1) + explore_faction * sqrt(2 * log(node.visits + 1) / (x.visits + 1))
    return max(bc, key=bc.get)




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
    new_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(state))
    node.child_nodes[new_node] = board.next_state(state, action)

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

    return board.points_values(state)


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

    if node.parent is None:
        return
    node.wins += won
    node.visits += 1
    backpropagate(node.parent, node.wins)

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
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

        for num_nodes_explore in range(num_nodes):
            node_explore = traverse_nodes(root_node, board, sampled_game, identity_of_bot)
            delta = rollout(board, sampled_game)
            if identity_of_bot == 1:
                backpropagate(node_explore, delta[1])
            else:
                backpropagate(node_explore, delta[2])
        return best_child(root_node).parent_action


    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
