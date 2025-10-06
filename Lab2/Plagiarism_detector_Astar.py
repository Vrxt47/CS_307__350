import heapq
import re

# Node class to store state information
class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from start
        self.h = h  # Heuristic (estimated cost to goal)
        self.f = g + h # Total cost

    # Allows nodes to be compared in the priority queue
    def __lt__(self, other):
        return self.f < other.f

def clean_text(text):
    """Removes punctuation and converts to lowercase."""
    return re.sub(r'[^\w\s]', '', text.lower())

def levenshtein(s1, s2):
    """Calculates the Levenshtein distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Cost of deleting all chars of s1 to get "" is i
    for i in range(m + 1):
        dp[i][0] = i
    # Cost of inserting all chars of s2 into "" is j
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,        # Deletion
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution

    return dp[m][n]

def astar(doc1, doc2, gap_penalty=50):
    """
    Finds the optimal alignment path using A* search with an admissible heuristic.
    """
    start_state = (0, 0)
    goal_state = (len(doc1), len(doc2))

    # --- Admissible Heuristic Function ---
    def heuristic(state):
        i, j = state
        remaining_in_doc1 = len(doc1) - i
        remaining_in_doc2 = len(doc2) - j
        # The cost of the guaranteed gaps
        return abs(remaining_in_doc1 - remaining_in_doc2) * gap_penalty

    start_node = Node(start_state, g=0, h=heuristic(start_state))

    open_list = [start_node] # Priority queue
    g_scores = {start_state: 0} # Stores the cheapest path to a state

    while open_list:
        n = heapq.heappop(open_list)

        if n.state == goal_state:
            return reconstruct_path(n)

        # Generate successors
        parent_idx1, parent_idx2 = n.state

        # Successor 1: Diagonal move
        if parent_idx1 < len(doc1) and parent_idx2 < len(doc2):
            s_state = (parent_idx1 + 1, parent_idx2 + 1)
            move_cost = levenshtein(doc1[parent_idx1], doc2[parent_idx2])
            new_g = n.g + move_cost
            if new_g < g_scores.get(s_state, float('inf')):
                g_scores[s_state] = new_g
                s_node = Node(s_state, n, new_g, heuristic(s_state))
                heapq.heappush(open_list, s_node)

        if parent_idx1 < len(doc1):
            s_state = (parent_idx1 + 1, parent_idx2)
            move_cost = gap_penalty
            new_g = n.g + move_cost
            if new_g < g_scores.get(s_state, float('inf')):
                g_scores[s_state] = new_g
                s_node = Node(s_state, n, new_g, heuristic(s_state))
                heapq.heappush(open_list, s_node)

        if parent_idx2 < len(doc2):
            s_state = (parent_idx1, parent_idx2 + 1)
            move_cost = gap_penalty
            new_g = n.g + move_cost
            if new_g < g_scores.get(s_state, float('inf')):
                g_scores[s_state] = new_g
                s_node = Node(s_state, n, new_g, heuristic(s_state))
                heapq.heappush(open_list, s_node)

    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def analyze_plagiarism(alignment, doc1, doc2, similarity_threshold=0.8):
    similar_pairs = []
    for k in range(len(alignment) - 1):
        p_state = alignment[k]
        c_state = alignment[k + 1]

        p_idx1, p_idx2 = p_state
        c_idx1, c_idx2 = c_state

        if c_idx1 > p_idx1 and c_idx2 > p_idx2:
            s1, s2 = doc1[p_idx1], doc2[p_idx2]
            max_len = max(len(s1), len(s2))

            if max_len > 0:
                dist = levenshtein(s1, s2)
                similarity = 1 - (dist / max_len)

                if similarity >= similarity_threshold:
                    similar_pairs.append((s1, s2, similarity))

    return similar_pairs


if __name__ == "__main__":
    """
    # --- Test Case 1: Identical Documents ---
    print("--- Running Test Case 1: Identical Documents ---")
    doc1 = [
        "The A* search algorithm is a popular pathfinding algorithm.",
        "It uses a heuristic to guide its search towards the goal state.",
        "This makes it more efficient than uninformed search methods."
    ]
    doc2 = [
        "The A* search algorithm is a popular pathfinding algorithm.",
        "It uses a heuristic to guide its search towards the goal state.",
        "This makes it more efficient than uninformed search methods."
    ]
    """
    """
    # --- Test Case 2: Slightly Modified Documents ---
    print("\n--- Running Test Case 2: Slightly Modified Documents ---")
    doc1 = [
        "The A* search algorithm is a popular pathfinding algorithm.",
        "It uses a heuristic to guide its search towards the goal state.",
        "This makes it more efficient than uninformed search methods."
    ]
    doc2 = [
        "A* search is a algorithm popular for finding paths.",
        "A heuristic is used to direct the search to the goal.",
        "It is more efficeint thean uninformed search methods."
    ]
    """


    # --- Test Case 3: Completely Different Documents ---
    print("\n--- Running Test Case 3: Completely Different Documents ---")
    doc1 = [
        "The A* search algorithm is a popular pathfinding algorithm.",
        "It uses a heuristic to guide its search towards the goal state.",
        "This makes it more efficient than uninformed search methods."
    ]
    doc2 = [
        "Photosynthesis is the process used by plants to convert light energy.",
        "Chlorophyll is the primary pigment used in this process.",
        "It produces oxygen as a byproduct."
    ]


    """
    # --- Test Case 4: Partial Overlapping Documents ---
    print("\n--- Running Test Case 4: Partial Overlapping Documents ---")
    doc1 = [
        "Artificial intelligence is a broad field of computer science.",
        "The A* search algorithm is a popular pathfinding algorithm.",
        "Machine learning is a subset of AI."
    ]
    doc2 = [
        "There are many algorithms for graph traversal.",
        "The A* search algorithm is a very popular pathfinding algorithm.",
        "Understanding data structures is also very important."
    ]
    """

    # --- Common processing for the selected test case ---
    cleaned_doc1 = [clean_text(sent) for sent in doc1]
    cleaned_doc2 = [clean_text(sent) for sent in doc2]

    alignment_path = astar(cleaned_doc1, cleaned_doc2, gap_penalty=30)

    if alignment_path:
        plagiarism_results = analyze_plagiarism(alignment_path, cleaned_doc1, cleaned_doc2, similarity_threshold=0.7)
        if plagiarism_results:
            print("Potential plagiarism detected:")
            for s1, s2, sim in plagiarism_results:
                print("-" * 20)
                print(f"Similarity: {sim*100:.2f}%")
                print(f"Doc1: '{s1}'")
                print(f"Doc2: '{s2}'")
        else:
            print("No significant plagiarism detected.")
    else:
        print("Could not find an alignment path.")