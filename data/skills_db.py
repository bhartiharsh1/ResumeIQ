# ============================================================
# SKILLS DATABASE — ResumeIQ Platform
# All profiles with SEO-optimized, ATS-verified keyword sets
# Format: { "Skill Display Name": ["keyword1", "keyword2", ...] }
# ============================================================

SKILLS_DB = {

    # ------------------------------------------------------------------ #
    #  DATA SCIENTIST
    # ------------------------------------------------------------------ #
    "Data Scientist": {
        "Python":               ["python", "py"],
        "R":                    ["r programming", " r ", "rstudio", "tidyverse"],
        "Machine Learning":     ["machine learning", "ml", "supervised learning", "unsupervised learning"],
        "Deep Learning":        ["deep learning", "neural network", "cnn", "rnn", "lstm", "transformer"],
        "TensorFlow":           ["tensorflow", "tf", "keras"],
        "PyTorch":              ["pytorch", "torch"],
        "Scikit-learn":         ["scikit-learn", "sklearn", "scikit learn"],
        "Statistics":           ["statistics", "statistical analysis", "hypothesis testing", "regression", "anova"],
        "Data Wrangling":       ["pandas", "numpy", "data wrangling", "data cleaning", "etl"],
        "SQL":                  ["sql", "mysql", "postgresql", "sqlite", "database query"],
        "Data Visualization":   ["matplotlib", "seaborn", "plotly", "tableau", "power bi", "visualization"],
        "Feature Engineering":  ["feature engineering", "feature selection", "dimensionality reduction", "pca"],
        "NLP":                  ["nlp", "natural language processing", "text mining", "sentiment analysis", "bert", "spacy", "nltk"],
        "Big Data":             ["spark", "hadoop", "hive", "pyspark", "big data", "databricks"],
        "Cloud Platforms":      ["aws", "gcp", "azure", "sagemaker", "bigquery", "google cloud"],
        "Model Deployment":     ["mlflow", "fastapi", "flask", "docker", "model deployment", "serving"],
        "Experiment Tracking":  ["mlflow", "wandb", "experiment tracking", "a/b testing"],
        "Version Control":      ["git", "github", "gitlab", "version control"],
        "Jupyter":              ["jupyter", "notebook", "colab", "google colab"],
        "Business Acumen":      ["kpi", "business intelligence", "roi", "stakeholder", "decision making"],
    },

    # ------------------------------------------------------------------ #
    #  DATA ANALYST
    # ------------------------------------------------------------------ #
    "Data Analyst": {
        "SQL":                  ["sql", "mysql", "postgresql", "tsql", "oracle sql", "sql server"],
        "Excel":                ["excel", "microsoft excel", "pivot table", "vlookup", "xlookup", "power query"],
        "Python":               ["python", "pandas", "numpy"],
        "Power BI":             ["power bi", "powerbi", "dax", "power query"],
        "Tableau":              ["tableau", "tableau desktop", "tableau public"],
        "Data Cleaning":        ["data cleaning", "data wrangling", "data quality", "etl", "data pipeline"],
        "Statistics":           ["statistics", "statistical analysis", "descriptive statistics", "regression", "correlation"],
        "Google Analytics":     ["google analytics", "ga4", "google data studio", "looker studio"],
        "Business Intelligence":["business intelligence", "bi", "kpi", "dashboard", "reporting"],
        "Data Storytelling":    ["data storytelling", "data presentation", "insights", "narrative"],
        "Looker":               ["looker", "looker studio", "lookml"],
        "R":                    ["r programming", "rstudio", "ggplot"],
        "Azure / AWS":          ["aws", "azure", "redshift", "snowflake", "bigquery"],
        "A/B Testing":          ["a/b testing", "hypothesis testing", "statistical significance"],
        "Spreadsheets":         ["google sheets", "spreadsheet", "airtable"],
        "Version Control":      ["git", "github", "version control"],
        "ETL Tools":            ["etl", "airflow", "talend", "informatica", "dbt"],
        "Communication":        ["stakeholder", "presentation", "reporting", "executive summary"],
    },

    # ------------------------------------------------------------------ #
    #  MACHINE LEARNING ENGINEER
    # ------------------------------------------------------------------ #
    "Machine Learning Engineer": {
        "Python":               ["python", "py"],
        "ML Frameworks":        ["tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost", "lightgbm"],
        "Deep Learning":        ["deep learning", "neural network", "cnn", "rnn", "lstm", "transformer", "attention mechanism"],
        "MLOps":                ["mlops", "mlflow", "kubeflow", "dvc", "model monitoring", "model registry"],
        "Model Deployment":     ["model deployment", "fastapi", "flask", "triton", "torchserve", "bentoml", "serving"],
        "Docker / Kubernetes":  ["docker", "kubernetes", "k8s", "containerization", "helm"],
        "CI/CD for ML":         ["ci/cd", "github actions", "jenkins", "automated pipeline", "continuous integration"],
        "Feature Engineering":  ["feature engineering", "feature store", "feast", "tecton"],
        "Data Pipelines":       ["airflow", "prefect", "luigi", "data pipeline", "etl", "spark"],
        "Cloud ML":             ["sagemaker", "vertex ai", "azure ml", "gcp", "aws", "cloud"],
        "SQL / NoSQL":          ["sql", "postgresql", "mongodb", "redis", "cassandra"],
        "Experiment Tracking":  ["mlflow", "wandb", "neptune", "experiment tracking"],
        "Statistics":           ["statistics", "probability", "bayesian", "hypothesis testing"],
        "Computer Vision":      ["opencv", "yolo", "resnet", "object detection", "image classification"],
        "NLP":                  ["nlp", "bert", "gpt", "huggingface", "transformers", "llm"],
        "Version Control":      ["git", "github", "gitlab", "version control"],
        "System Design":        ["system design", "scalability", "microservices", "rest api"],
        "Linux":                ["linux", "bash", "shell scripting", "unix"],
    },

    # ------------------------------------------------------------------ #
    #  AI ENGINEER
    # ------------------------------------------------------------------ #
    "AI Engineer": {
        "Python":               ["python", "py"],
        "LLMs":                 ["llm", "large language model", "gpt", "claude", "gemini", "llama", "mistral"],
        "Prompt Engineering":   ["prompt engineering", "chain of thought", "few shot", "zero shot", "rag", "retrieval augmented"],
        "LangChain / LlamaIndex":["langchain", "llamaindex", "llama index", "langraph", "agent framework"],
        "Hugging Face":         ["huggingface", "hugging face", "transformers", "diffusers", "datasets"],
        "Vector Databases":     ["pinecone", "weaviate", "chroma", "qdrant", "faiss", "vector database", "embedding store"],
        "Fine-tuning":          ["fine tuning", "fine-tuning", "lora", "qlora", "peft", "rlhf", "instruction tuning"],
        "APIs":                 ["openai api", "anthropic api", "rest api", "api integration"],
        "Computer Vision":      ["opencv", "yolo", "stable diffusion", "diffusion model", "image generation", "dalle"],
        "Deep Learning":        ["tensorflow", "pytorch", "neural network", "cnn", "transformer"],
        "Cloud Deployment":     ["aws", "gcp", "azure", "lambda", "cloud functions", "sagemaker"],
        "Docker / Kubernetes":  ["docker", "kubernetes", "k8s", "containerization"],
        "MLOps":                ["mlops", "mlflow", "kubeflow", "model monitoring"],
        "Evaluation Metrics":   ["evaluation", "benchmarking", "ragas", "lm-eval", "model evaluation"],
        "Agent Frameworks":     ["autogen", "crewai", "langraph", "agentic", "autonomous agent"],
        "Version Control":      ["git", "github", "version control"],
        "FastAPI / Flask":      ["fastapi", "flask", "api development", "rest"],
        "SQL / Databases":      ["sql", "postgresql", "mongodb", "sqlite"],
    },

    # ------------------------------------------------------------------ #
    #  SOFTWARE ENGINEER
    # ------------------------------------------------------------------ #
    "Software Engineer": {
        "DSA":                  ["data structures", "algorithms", "dsa", "dynamic programming", "graph", "tree", "binary search"],
        "Python":               ["python", "py"],
        "Java":                 ["java", "jdk", "spring", "maven", "gradle"],
        "C++":                  ["c++", "cpp", "stl", "competitive programming"],
        "System Design":        ["system design", "scalability", "high availability", "load balancer", "microservices"],
        "OOP":                  ["oop", "object oriented", "design patterns", "solid principles"],
        "Databases":            ["sql", "mysql", "postgresql", "mongodb", "redis", "nosql"],
        "REST APIs":            ["rest api", "restful", "api design", "http", "openapi", "swagger"],
        "Git / Version Control":["git", "github", "gitlab", "version control", "pull request", "code review"],
        "Testing":              ["unit testing", "integration testing", "tdd", "jest", "pytest", "junit"],
        "Docker / CI/CD":       ["docker", "ci/cd", "github actions", "jenkins", "pipeline"],
        "Cloud":                ["aws", "gcp", "azure", "cloud", "s3", "ec2", "lambda"],
        "Operating Systems":    ["linux", "unix", "bash", "shell", "os"],
        "Multithreading":       ["multithreading", "concurrency", "async", "parallel programming"],
        "Networking":           ["tcp/ip", "http", "dns", "networking", "socket"],
        "Problem Solving":      ["leetcode", "competitive programming", "hackerrank", "codeforces"],
    },

    # ------------------------------------------------------------------ #
    #  BACKEND DEVELOPER
    # ------------------------------------------------------------------ #
    "Backend Developer": {
        "Python":               ["python", "django", "flask", "fastapi"],
        "Node.js":              ["node.js", "nodejs", "express", "express.js", "nestjs"],
        "Java":                 ["java", "spring boot", "spring", "hibernate", "maven"],
        "Go":                   ["golang", "go lang", "gin", "fiber"],
        "REST APIs":            ["rest api", "restful", "api design", "openapi", "swagger", "graphql"],
        "Databases (SQL)":      ["sql", "mysql", "postgresql", "oracle", "mariadb"],
        "Databases (NoSQL)":    ["mongodb", "redis", "cassandra", "dynamodb", "nosql", "firebase"],
        "Authentication":       ["jwt", "oauth", "oauth2", "authentication", "authorization", "keycloak"],
        "Message Queues":       ["kafka", "rabbitmq", "celery", "message queue", "pub/sub", "sqs"],
        "Caching":              ["redis", "memcached", "caching strategy", "cdn"],
        "Docker / Kubernetes":  ["docker", "kubernetes", "k8s", "containerization", "helm"],
        "CI/CD":                ["ci/cd", "github actions", "jenkins", "gitlab ci", "automated deployment"],
        "Cloud":                ["aws", "gcp", "azure", "ec2", "s3", "rds", "cloud"],
        "System Design":        ["system design", "microservices", "monolith", "distributed systems", "scalability"],
        "Testing":              ["unit testing", "pytest", "junit", "postman", "integration testing"],
        "Linux":                ["linux", "bash", "shell scripting", "unix", "nginx"],
        "Version Control":      ["git", "github", "gitlab", "version control"],
        "ORM":                  ["orm", "sqlalchemy", "typeorm", "prisma", "sequelize", "hibernate"],
    },

    # ------------------------------------------------------------------ #
    #  FRONTEND DEVELOPER
    # ------------------------------------------------------------------ #
    "Frontend Developer": {
        "HTML / CSS":           ["html", "css", "html5", "css3", "semantic html"],
        "JavaScript":           ["javascript", "js", "es6", "es2015", "ecmascript"],
        "TypeScript":           ["typescript", "ts"],
        "React.js":             ["react", "reactjs", "react.js", "jsx", "hooks", "redux", "context api"],
        "Next.js":              ["next.js", "nextjs", "next", "ssr", "server side rendering"],
        "Vue.js":               ["vue", "vue.js", "vuejs", "nuxt", "pinia", "vuex"],
        "Angular":              ["angular", "angularjs", "typescript", "rxjs", "ng"],
        "Responsive Design":    ["responsive design", "mobile first", "flexbox", "grid", "media query"],
        "CSS Frameworks":       ["tailwind", "tailwindcss", "bootstrap", "material ui", "chakra ui", "shadcn"],
        "State Management":     ["redux", "zustand", "recoil", "mobx", "context api", "state management"],
        "API Integration":      ["rest api", "graphql", "axios", "fetch", "api integration"],
        "Testing":              ["jest", "react testing library", "cypress", "playwright", "unit testing"],
        "Build Tools":          ["webpack", "vite", "rollup", "parcel", "babel"],
        "Version Control":      ["git", "github", "gitlab", "version control"],
        "Performance":          ["web vitals", "lighthouse", "lazy loading", "code splitting", "performance optimization"],
        "Accessibility":        ["accessibility", "a11y", "wcag", "aria", "screen reader"],
        "CI/CD":                ["ci/cd", "github actions", "vercel", "netlify", "deployment"],
        "Design Tools":         ["figma", "zeplin", "adobe xd", "storybook"],
    },

    # ------------------------------------------------------------------ #
    #  FULL STACK DEVELOPER
    # ------------------------------------------------------------------ #
    "Full Stack Developer": {
        "HTML / CSS":           ["html", "css", "html5", "css3"],
        "JavaScript":           ["javascript", "js", "typescript", "ts"],
        "React / Next.js":      ["react", "reactjs", "next.js", "nextjs", "vue", "angular"],
        "Node.js / Express":    ["node.js", "nodejs", "express", "express.js", "nestjs"],
        "Python Backend":       ["python", "django", "flask", "fastapi"],
        "REST APIs / GraphQL":  ["rest api", "restful", "graphql", "api design"],
        "SQL Databases":        ["sql", "mysql", "postgresql", "sqlite"],
        "NoSQL Databases":      ["mongodb", "firebase", "dynamodb", "redis", "nosql"],
        "Authentication":       ["jwt", "oauth", "authentication", "session", "passport.js"],
        "Docker":               ["docker", "containerization", "docker compose"],
        "Cloud / Hosting":      ["aws", "gcp", "azure", "vercel", "netlify", "heroku", "cloud"],
        "Version Control":      ["git", "github", "gitlab", "version control"],
        "Testing":              ["jest", "pytest", "cypress", "unit testing", "integration testing"],
        "CI/CD":                ["ci/cd", "github actions", "gitlab ci", "automated deployment"],
        "State Management":     ["redux", "zustand", "context api", "state management"],
        "CSS Frameworks":       ["tailwind", "bootstrap", "material ui"],
        "ORMs":                 ["prisma", "sequelize", "typeorm", "sqlalchemy", "mongoose"],
        "System Design":        ["system design", "microservices", "scalability"],
    },

    # ------------------------------------------------------------------ #
    #  DEVOPS ENGINEER
    # ------------------------------------------------------------------ #
    "DevOps Engineer": {
        "Linux / Bash":         ["linux", "bash", "shell scripting", "unix", "ubuntu", "centos"],
        "Docker":               ["docker", "dockerfile", "docker compose", "containerization"],
        "Kubernetes":           ["kubernetes", "k8s", "helm", "kubectl", "pod", "deployment", "service mesh"],
        "CI/CD":                ["ci/cd", "jenkins", "github actions", "gitlab ci", "circleci", "argocd", "spinnaker"],
        "Infrastructure as Code":["terraform", "ansible", "pulumi", "cloudformation", "iac"],
        "Cloud (AWS)":          ["aws", "ec2", "s3", "rds", "lambda", "vpc", "iam", "eks", "ecs"],
        "Cloud (GCP/Azure)":    ["gcp", "azure", "gke", "aks", "cloud run", "google cloud"],
        "Monitoring":           ["prometheus", "grafana", "datadog", "elk stack", "cloudwatch", "monitoring", "alerting"],
        "Logging":              ["elk", "elasticsearch", "logstash", "kibana", "splunk", "loki", "logging"],
        "Networking":           ["tcp/ip", "dns", "load balancer", "nginx", "vpc", "firewall", "networking"],
        "Security (DevSecOps)": ["devsecops", "vault", "iam", "secrets management", "sonarqube", "security scanning"],
        "Git":                  ["git", "github", "gitlab", "bitbucket", "version control"],
        "Service Mesh":         ["istio", "envoy", "linkerd", "service mesh"],
        "Scripting":            ["python", "bash", "groovy", "scripting", "automation"],
        "Artifact Management":  ["jfrog", "nexus", "artifactory", "harbor", "container registry"],
        "Agile / Scrum":        ["agile", "scrum", "jira", "kanban", "sprint"],
    },

    # ------------------------------------------------------------------ #
    #  CLOUD ENGINEER
    # ------------------------------------------------------------------ #
    "Cloud Engineer": {
        "AWS":                  ["aws", "amazon web services", "ec2", "s3", "rds", "lambda", "cloudformation", "eks", "vpc", "iam"],
        "Azure":                ["azure", "microsoft azure", "aks", "azure functions", "azure devops", "arm template"],
        "GCP":                  ["gcp", "google cloud", "gke", "cloud run", "bigquery", "pubsub", "firestore"],
        "Terraform":            ["terraform", "infrastructure as code", "iac", "hcl"],
        "Kubernetes":           ["kubernetes", "k8s", "helm", "kubectl", "eks", "aks", "gke"],
        "Docker":               ["docker", "containerization", "docker compose"],
        "Networking":           ["vpc", "subnet", "load balancer", "cdn", "dns", "firewall", "networking", "route53"],
        "Cloud Security":       ["iam", "cloud security", "kms", "encryption", "compliance", "zero trust"],
        "Serverless":           ["lambda", "cloud functions", "azure functions", "serverless", "faas"],
        "Databases (Cloud)":    ["rds", "aurora", "dynamodb", "cloud sql", "cosmos db", "cloud database"],
        "CI/CD":                ["ci/cd", "github actions", "jenkins", "argocd", "azure devops", "cloud build"],
        "Monitoring":           ["cloudwatch", "azure monitor", "stackdriver", "prometheus", "datadog", "monitoring"],
        "Storage":              ["s3", "azure blob", "gcs", "cloud storage", "object storage"],
        "Linux / Bash":         ["linux", "bash", "shell scripting", "unix"],
        "Python / Scripting":   ["python", "boto3", "scripting", "automation"],
        "Cost Optimization":    ["cost optimization", "cost management", "reserved instances", "spot instances", "finops"],
        "Certifications":       ["aws certified", "azure certified", "gcp certified", "cloud certification", "ccp", "saa", "sap"],
    },

    # ------------------------------------------------------------------ #
    #  CYBERSECURITY ANALYST
    # ------------------------------------------------------------------ #
    "Cybersecurity Analyst": {
        "Network Security":     ["network security", "firewall", "ids", "ips", "vpn", "packet analysis", "wireshark", "tcp/ip"],
        "SIEM":                 ["siem", "splunk", "ibm qradar", "microsoft sentinel", "elastic siem", "log management"],
        "Penetration Testing":  ["penetration testing", "pentest", "pen test", "metasploit", "burp suite", "kali linux"],
        "Vulnerability Assessment":["vulnerability assessment", "nessus", "qualys", "openvas", "nmap", "vulnerability scanning"],
        "Incident Response":    ["incident response", "digital forensics", "threat hunting", "ir", "soc"],
        "Threat Intelligence":  ["threat intelligence", "mitre att&ck", "ioc", "threat hunting", "cyber threat"],
        "Cloud Security":       ["cloud security", "aws security", "azure security", "iam", "cspm", "cwpp"],
        "Cryptography":         ["cryptography", "encryption", "ssl", "tls", "pki", "hashing"],
        "Compliance":           ["compliance", "iso 27001", "gdpr", "hipaa", "pci dss", "nist", "sox"],
        "Ethical Hacking":      ["ethical hacking", "ceh", "oscp", "bug bounty", "ctf", "red team", "blue team"],
        "Python / Scripting":   ["python", "bash", "powershell", "scripting", "automation"],
        "Endpoint Security":    ["endpoint security", "edr", "antivirus", "crowdstrike", "sentinelone", "carbon black"],
        "SOC Operations":       ["soc", "security operations", "alert triage", "playbook", "soar"],
        "Linux":                ["linux", "kali linux", "ubuntu", "bash", "unix"],
        "Programming":          ["python", "c", "c++", "assembly", "reverse engineering"],
        "Zero Trust":           ["zero trust", "zero trust architecture", "ztna", "least privilege"],
        "Certifications":       ["cissp", "ceh", "oscp", "comptia security+", "cism", "ccna security"],
    },

    # ------------------------------------------------------------------ #
    #  PRODUCT MANAGER
    # ------------------------------------------------------------------ #
    "Product Manager": {
        "Product Strategy":     ["product strategy", "product vision", "roadmap", "product roadmap", "okr", "kpi"],
        "Agile / Scrum":        ["agile", "scrum", "sprint", "kanban", "jira", "confluence", "backlog"],
        "User Research":        ["user research", "user interview", "usability testing", "ux research", "customer discovery"],
        "Data Analysis":        ["data analysis", "sql", "google analytics", "mixpanel", "amplitude", "funnel analysis"],
        "A/B Testing":          ["a/b testing", "experimentation", "hypothesis testing", "statistical significance"],
        "Wireframing":          ["wireframing", "figma", "balsamiq", "prototype", "mockup", "ux design"],
        "Stakeholder Management":["stakeholder management", "cross-functional", "alignment", "executive presentation"],
        "Go-to-Market":         ["go-to-market", "gtm", "product launch", "market research", "competitive analysis"],
        "User Stories":         ["user stories", "acceptance criteria", "epics", "backlog grooming", "sprint planning"],
        "Metrics & KPIs":       ["metrics", "kpi", "dau", "mau", "retention", "churn", "ltv", "cac", "nps"],
        "PRD Writing":          ["prd", "product requirements", "brd", "specification document", "feature spec"],
        "Customer Empathy":     ["customer empathy", "design thinking", "jobs to be done", "pain point", "persona"],
        "Prioritization":       ["prioritization", "rice framework", "moscow", "value vs effort", "feature prioritization"],
        "Technical Knowledge":  ["api", "sdk", "technical feasibility", "system design", "engineering collaboration"],
        "Communication":        ["communication", "presentation", "storytelling", "executive stakeholder", "product demo"],
        "CRM / Tools":          ["salesforce", "hubspot", "intercom", "zendesk", "notion", "productboard", "aha"],
    },

    # ------------------------------------------------------------------ #
    #  BUSINESS ANALYST
    # ------------------------------------------------------------------ #
    "Business Analyst": {
        "Requirements Gathering":["requirements gathering", "brd", "frd", "functional requirements", "business requirements"],
        "SQL":                  ["sql", "mysql", "postgresql", "database queries", "data extraction"],
        "Excel / Spreadsheets": ["excel", "pivot table", "vlookup", "power query", "google sheets", "spreadsheet"],
        "Data Analysis":        ["data analysis", "data analytics", "statistical analysis", "trend analysis"],
        "Business Intelligence":["power bi", "tableau", "looker", "business intelligence", "dashboard", "reporting"],
        "Process Mapping":      ["process mapping", "bpmn", "flowchart", "swim lane", "as-is to-be", "process improvement"],
        "Stakeholder Management":["stakeholder management", "stakeholder communication", "client liaison", "meeting facilitation"],
        "Agile / Scrum":        ["agile", "scrum", "jira", "confluence", "sprint", "backlog"],
        "Use Case Modeling":    ["use case", "uml", "sequence diagram", "activity diagram", "user story"],
        "Gap Analysis":         ["gap analysis", "root cause analysis", "swot", "impact analysis", "as-is"],
        "Financial Modeling":   ["financial modeling", "budgeting", "forecasting", "roi analysis", "cost benefit"],
        "ERP Systems":          ["sap", "oracle erp", "salesforce", "dynamics 365", "erp"],
        "Testing / UAT":        ["uat", "user acceptance testing", "test cases", "qa", "regression testing"],
        "Communication":        ["communication", "presentation", "executive reporting", "documentation"],
        "Project Management":   ["project management", "pmp", "waterfall", "prince2", "ms project"],
        "Python / R":           ["python", "r programming", "automation", "data scripting"],
    },

    # ------------------------------------------------------------------ #
    #  UI/UX DESIGNER
    # ------------------------------------------------------------------ #
    "UI/UX Designer": {
        "Figma":                ["figma", "figma design", "autolayout", "figma prototype", "figma components"],
        "User Research":        ["user research", "user interview", "contextual inquiry", "ethnographic research", "diary study"],
        "Wireframing":          ["wireframing", "low fidelity", "lo-fi", "sketching", "wireframe"],
        "Prototyping":          ["prototyping", "interactive prototype", "high fidelity", "clickable prototype"],
        "Usability Testing":    ["usability testing", "moderated testing", "unmoderated testing", "user testing", "a/b test"],
        "Information Architecture":["information architecture", "ia", "card sorting", "tree testing", "sitemap"],
        "Interaction Design":   ["interaction design", "ixd", "micro-interactions", "motion design", "animation"],
        "Visual Design":        ["visual design", "typography", "color theory", "iconography", "brand design", "ui design"],
        "Design Systems":       ["design system", "component library", "style guide", "atomic design", "storybook"],
        "Adobe Suite":          ["adobe xd", "photoshop", "illustrator", "after effects", "adobe suite"],
        "HTML / CSS":           ["html", "css", "tailwind", "responsive design", "frontend basics"],
        "Accessibility":        ["accessibility", "wcag", "a11y", "inclusive design", "aria"],
        "Heuristic Evaluation": ["heuristic evaluation", "cognitive walkthrough", "expert review", "ux audit"],
        "User Personas":        ["user persona", "empathy map", "customer journey", "journey mapping", "user flow"],
        "Design Thinking":      ["design thinking", "double diamond", "ideation", "brainstorming", "co-design"],
        "Collaboration Tools":  ["miro", "mural", "notion", "jira", "confluence", "zeplin", "abstract"],
        "Mobile Design":        ["mobile design", "ios", "android", "responsive", "material design", "human interface guidelines"],
    },

    # ------------------------------------------------------------------ #
    #  MOBILE APP DEVELOPER
    # ------------------------------------------------------------------ #
    "Mobile App Developer": {
        "Android (Kotlin)":     ["kotlin", "android", "jetpack compose", "android studio", "android sdk"],
        "iOS (Swift)":          ["swift", "ios", "swiftui", "xcode", "cocoa touch", "uikit"],
        "React Native":         ["react native", "reactnative", "expo", "react native cli"],
        "Flutter":              ["flutter", "dart", "flutter sdk", "flutter widgets"],
        "REST API Integration": ["rest api", "api integration", "retrofit", "alamofire", "http", "graphql"],
        "State Management":     ["state management", "bloc", "riverpod", "redux", "provider", "getx", "mobx"],
        "Firebase":             ["firebase", "firestore", "firebase auth", "fcm", "cloud messaging", "crashlytics"],
        "Push Notifications":   ["push notifications", "fcm", "apns", "firebase messaging", "local notifications"],
        "UI / UX Mobile":       ["jetpack compose", "swiftui", "material design", "human interface guidelines", "animations"],
        "SQLite / Local DB":    ["sqlite", "room database", "core data", "realm", "local storage", "shared preferences"],
        "CI/CD Mobile":         ["fastlane", "bitrise", "codemagic", "github actions", "app center", "ci/cd"],
        "App Store Deployment": ["google play", "app store", "app store connect", "play console", "app signing"],
        "Testing (Mobile)":     ["unit testing", "ui testing", "espresso", "xctest", "detox", "appium"],
        "Performance":          ["performance optimization", "memory management", "profiling", "app size", "startup time"],
        "Version Control":      ["git", "github", "gitlab", "version control"],
        "Background Services":  ["background service", "workmanager", "background fetch", "job scheduler"],
        "Security (Mobile)":    ["ssl pinning", "certificate pinning", "keychain", "obfuscation", "proguard"],
    },
}