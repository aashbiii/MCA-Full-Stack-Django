from django.shortcuts import render, get_object_or_404
from django.http import Http404

# ── In-memory blog data (no database) ─────────────────────────────────────────
POSTS = [
    {
        "id": 1,
        "title": "Getting Started with Python",
        "slug": "getting-started-with-python",
        "author": "Alice Chen",
        "category": "Programming",
        "date": "March 01, 2026",
        "read_time": "5 min read",
        "excerpt": "Python is one of the most beginner-friendly languages out there. In this post, we explore why Python is the perfect first language and how to set it up on your machine.",
        "content": """
Python is a high-level, interpreted programming language known for its simplicity and readability.
Created by Guido van Rossum in 1991, it has become one of the most popular languages in the world.

<h3>Why Python?</h3>
<ul>
  <li>Clean and readable syntax</li>
  <li>Huge standard library</li>
  <li>Massive community support</li>
  <li>Used in web dev, data science, AI, automation, and more</li>
</ul>

<h3>Installing Python</h3>
<p>Visit <strong>python.org</strong> and download the latest version. Run the installer and make sure to check "Add Python to PATH".</p>

<h3>Your First Program</h3>
<pre><code>print("Hello, World!")</code></pre>

<p>That's it! You've written your first Python program. From here, the sky is the limit.</p>
        """,
        "tags": ["Python", "Beginners", "Programming"],
        "image_color": "#667eea",
        "image_emoji": "🐍",
    },
    {
        "id": 2,
        "title": "Understanding Django MVT Architecture",
        "slug": "django-mvt-architecture",
        "author": "Bob Sharma",
        "category": "Web Development",
        "date": "February 22, 2026",
        "read_time": "7 min read",
        "excerpt": "Django follows the MVT (Model-View-Template) pattern. Understanding this architecture is key to building powerful web applications with Django.",
        "content": """
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

<h3>What is MVT?</h3>
<p>MVT stands for <strong>Model-View-Template</strong>:</p>
<ul>
  <li><strong>Model</strong> — Handles data and database logic</li>
  <li><strong>View</strong> — Handles business logic and returns responses</li>
  <li><strong>Template</strong> — Handles the HTML presentation layer</li>
</ul>

<h3>How a Request Works</h3>
<p>When a user visits a URL:</p>
<ol>
  <li>Django's URL dispatcher routes the request to a View</li>
  <li>The View queries the Model if needed</li>
  <li>The View passes data to a Template</li>
  <li>The Template renders HTML and sends it back</li>
</ol>

<h3>Why MVT over MVC?</h3>
<p>In Django, the "Controller" role is shared between the URL dispatcher and the View. This separation makes the code cleaner and easier to maintain.</p>
        """,
        "tags": ["Django", "Web", "Architecture"],
        "image_color": "#11998e",
        "image_emoji": "🏗️",
    },
    {
        "id": 3,
        "title": "CSS Grid vs Flexbox: When to Use Which",
        "slug": "css-grid-vs-flexbox",
        "author": "Clara Gomez",
        "category": "Design",
        "date": "February 15, 2026",
        "read_time": "6 min read",
        "excerpt": "Both CSS Grid and Flexbox are powerful layout tools, but they serve different purposes. Here's a clear guide on when to reach for each one.",
        "content": """
CSS Grid and Flexbox are both excellent layout systems, but they shine in different scenarios.

<h3>Flexbox — One Dimension</h3>
<p>Use Flexbox when you need to lay out items in a <strong>single row or column</strong>.</p>
<ul>
  <li>Navigation bars</li>
  <li>Centering an element</li>
  <li>Distributing space between items</li>
</ul>

<h3>CSS Grid — Two Dimensions</h3>
<p>Use Grid when you need to control both <strong>rows and columns</strong> simultaneously.</p>
<ul>
  <li>Page layouts</li>
  <li>Card grids</li>
  <li>Complex dashboard layouts</li>
</ul>

<h3>The Golden Rule</h3>
<p>Use <strong>Grid for the layout</strong> of the page, and <strong>Flexbox for the components</strong> within that layout. They work beautifully together!</p>
        """,
        "tags": ["CSS", "Design", "Frontend"],
        "image_color": "#f7971e",
        "image_emoji": "🎨",
    },
    {
        "id": 4,
        "title": "Introduction to Machine Learning",
        "slug": "intro-to-machine-learning",
        "author": "David Park",
        "category": "AI & ML",
        "date": "February 08, 2026",
        "read_time": "8 min read",
        "excerpt": "Machine Learning is transforming every industry. This beginner-friendly post explains the core concepts — supervised, unsupervised, and reinforcement learning.",
        "content": """
Machine Learning (ML) is a subset of Artificial Intelligence that allows systems to learn from data.

<h3>Types of Machine Learning</h3>
<ul>
  <li><strong>Supervised Learning</strong> — The model learns from labeled data (e.g., spam detection)</li>
  <li><strong>Unsupervised Learning</strong> — The model finds patterns in unlabeled data (e.g., clustering)</li>
  <li><strong>Reinforcement Learning</strong> — The model learns through rewards and penalties (e.g., game playing AI)</li>
</ul>

<h3>Common Algorithms</h3>
<ol>
  <li>Linear Regression</li>
  <li>Decision Trees</li>
  <li>Neural Networks</li>
  <li>k-Nearest Neighbors</li>
</ol>

<h3>Getting Started</h3>
<p>The best library for beginners is <strong>scikit-learn</strong> in Python. Install it with:</p>
<pre><code>pip install scikit-learn</code></pre>
        """,
        "tags": ["ML", "AI", "Data Science"],
        "image_color": "#8e2de2",
        "image_emoji": "🤖",
    },
    {
        "id": 5,
        "title": "10 Tips for Clean Code",
        "slug": "10-tips-for-clean-code",
        "author": "Alice Chen",
        "category": "Programming",
        "date": "January 30, 2026",
        "read_time": "4 min read",
        "excerpt": "Writing clean code is an art. These 10 practical tips will make your codebase easier to read, maintain, and collaborate on.",
        "content": """
Clean code is code that is easy to understand, easy to change, and easy to test.

<h3>Top 10 Tips</h3>
<ol>
  <li><strong>Use meaningful variable names</strong> — <code>user_age</code> beats <code>x</code></li>
  <li><strong>Keep functions small</strong> — Each function should do one thing</li>
  <li><strong>Avoid deep nesting</strong> — Use early returns</li>
  <li><strong>Write comments for WHY, not WHAT</strong></li>
  <li><strong>DRY</strong> — Don't Repeat Yourself</li>
  <li><strong>KISS</strong> — Keep It Simple, Stupid</li>
  <li><strong>Handle errors gracefully</strong></li>
  <li><strong>Write tests</strong> — They are documentation too</li>
  <li><strong>Consistent formatting</strong> — Use a linter</li>
  <li><strong>Refactor regularly</strong> — Leave code better than you found it</li>
</ol>

<blockquote>"Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — Martin Fowler</blockquote>
        """,
        "tags": ["Clean Code", "Best Practices", "Tips"],
        "image_color": "#c94b4b",
        "image_emoji": "✨",
    },
    {
        "id": 6,
        "title": "REST API Design Best Practices",
        "slug": "rest-api-design-best-practices",
        "author": "Bob Sharma",
        "category": "Web Development",
        "date": "January 20, 2026",
        "read_time": "6 min read",
        "excerpt": "A well-designed REST API makes life easy for developers. These best practices will help you design APIs that are intuitive, consistent, and robust.",
        "content": """
REST (Representational State Transfer) is the most popular architectural style for building web APIs.

<h3>Core Principles</h3>
<ul>
  <li><strong>Use nouns for endpoints</strong> — <code>/users</code>, not <code>/getUsers</code></li>
  <li><strong>HTTP methods matter</strong> — GET (read), POST (create), PUT (update), DELETE (remove)</li>
  <li><strong>Use proper status codes</strong> — 200, 201, 400, 404, 500</li>
  <li><strong>Version your API</strong> — <code>/api/v1/users</code></li>
</ul>

<h3>Naming Conventions</h3>
<ul>
  <li>Use lowercase and hyphens: <code>/blog-posts</code></li>
  <li>Use plural nouns: <code>/posts</code> not <code>/post</code></li>
  <li>Nested resources: <code>/users/42/posts</code></li>
</ul>

<h3>Always Return JSON</h3>
<p>Include <code>Content-Type: application/json</code> in your response headers and always return a consistent JSON structure.</p>
        """,
        "tags": ["API", "REST", "Backend"],
        "image_color": "#1a1a2e",
        "image_emoji": "🔌",
    },
]

CATEGORIES = sorted(set(p["category"] for p in POSTS))


def get_post_by_slug(slug):
    for post in POSTS:
        if post["slug"] == slug:
            return post
    return None


# ── Views ──────────────────────────────────────────────────────────────────────

def home(request):
    category = request.GET.get("category", "")
    search = request.GET.get("search", "").strip()

    posts = POSTS
    if category:
        posts = [p for p in posts if p["category"] == category]
    if search:
        posts = [p for p in posts if search.lower() in p["title"].lower()
                 or search.lower() in p["excerpt"].lower()]

    return render(request, "blog/home.html", {
        "posts": posts,
        "categories": CATEGORIES,
        "active_category": category,
        "search": search,
        "total": len(POSTS),
    })


def post_detail(request, slug):
    post = get_post_by_slug(slug)
    if not post:
        raise Http404("Post not found")

    # Related posts: same category, exclude current
    related = [p for p in POSTS if p["category"] == post["category"] and p["slug"] != slug][:2]

    return render(request, "blog/detail.html", {
        "post": post,
        "related": related,
    })


def about(request):
    authors = {}
    for p in POSTS:
        authors[p["author"]] = authors.get(p["author"], 0) + 1
    return render(request, "blog/about.html", {
        "authors": authors,
        "total_posts": len(POSTS),
        "categories": CATEGORIES,
    })
