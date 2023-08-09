import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = corpus.keys()
    divided_compliment = (1 - damping_factor)/len(corpus)
    distribution = dict.fromkeys(pages, divided_compliment)

    if corpus[page] is None: 
        return distribution

    divided_proportion = damping_factor/len(corpus[page])

    for i in distribution:
        if(i in corpus[page]):
            distribution[i] += divided_proportion

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict.fromkeys(corpus.keys(), 0)
    page = random.choice(list(corpus.keys()))

    for i in range(n):  
        distribution = transition_model(corpus, page, damping_factor)
        #print("page: ", page)
        #print("distribution: ", distribution, "\n")
        weights = [int(float(i)*1000) for i in list(distribution.values())]
        selection = random.choices(list(distribution.keys()), weights = weights, k=1)[0]
        page_rank[selection] += 1
        page = selection
    
    page_rank = {i : page_rank[i]/n for i in page_rank}
    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = dict.fromkeys(corpus.keys(), 1/N)
    PR_copy = page_rank.copy()

    iterate = True
    while(iterate):
        for page in page_rank:
            summation = 0
            for i in corpus:
                if page in corpus[i]:
                    if(len(corpus[i]) == 0):
                        summation += page_rank[i]/len(corpus)
                        continue
                    summation += page_rank[i]/len(corpus[i])

            PR_copy[page] = (1-damping_factor)/N + damping_factor*summation

        passed = 0
        for page in page_rank:
            if abs(page_rank[page] - PR_copy[page]) > 0.001:
                iterate = True
            else:
                passed +=1
            
            if(passed == len(page_rank)):
                iterate = False

        page_rank = PR_copy.copy()
    return page_rank

if __name__ == "__main__":
    main()


""""""