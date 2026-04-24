def generate_roadmap(selected_profile, present_skills, missing_skills):

    roadmap = []

    HIGH = missing_skills[:3]

    # ---------------- DATA SCIENTIST ----------------
    if selected_profile == "Data Scientist":
        roadmap += [
            "🚀 PHASE 1: Core Foundation",
            *[f"→ Deep dive into {s}" for s in HIGH],
            "→ Strengthen statistics & probability (mean, variance, distributions, Bayes theorem)",
            "→ Master NumPy + Pandas for data manipulation",
            "\n🔥 PHASE 2: Practical Machine Learning",
            "→ Build 2 end-to-end ML projects (classification + regression)",
            "→ Learn Scikit-learn: pipelines, cross-validation, hyperparameter tuning",
            "→ Work on Kaggle datasets — compete in beginner competitions",
            "→ Master feature engineering + feature selection techniques",
            "\n💡 PHASE 3: Advanced Skills",
            "→ Learn deep learning fundamentals (CNNs, RNNs) with TensorFlow or PyTorch",
            "→ Explore NLP: text classification, sentiment analysis, BERT basics",
            "→ Learn model deployment: Flask / FastAPI + Docker",
            "→ Build end-to-end ML pipeline (data ingestion → training → serving)",
            "\n🏆 PHASE 4: Stand Out",
            "→ Publish all projects on GitHub with clear README + visuals",
            "→ Participate actively in Kaggle competitions (aim for top 20%)",
            "→ Write 2–3 Medium / Hashnode blogs on your ML findings",
            "→ Build a portfolio website showcasing dashboards + notebooks",
            "→ Target certifications: AWS ML Specialty / Google Professional ML Engineer",
        ]

    # ---------------- DATA ANALYST ----------------
    elif selected_profile == "Data Analyst":
        roadmap += [
            "🚀 PHASE 1: Core Tool Mastery",
            *[f"→ Master {s}" for s in HIGH],
            "→ Excel deep dive: Pivot Tables, VLOOKUP, Power Query, dynamic charts",
            "→ SQL mastery: complex JOINs, subqueries, CTEs, window functions",
            "\n🔥 PHASE 2: Business Analytics & Visualization",
            "→ Build interactive dashboards in Power BI and Tableau",
            "→ Analyze 3 real business datasets (e-commerce, marketing, finance)",
            "→ Learn Google Analytics 4 (GA4) and Looker Studio",
            "→ Connect data pipelines using basic ETL concepts (dbt, Airflow basics)",
            "\n💡 PHASE 3: Insight Communication",
            "→ Learn data storytelling: structure → insight → recommendation",
            "→ Focus on KPIs, OKRs, and business decision metrics",
            "→ Practice presenting findings to a non-technical audience",
            "→ Learn Python for automation: Pandas, Matplotlib, Seaborn",
            "\n🏆 PHASE 4: Portfolio & Placement",
            "→ Create 3 polished dashboard projects and publish on Tableau Public",
            "→ Write case studies for each project on LinkedIn",
            "→ Target Google Data Analytics or Microsoft Power BI certifications",
            "→ Apply for analyst internships and include portfolio link in resume",
        ]

    # ---------------- ML ENGINEER ----------------
    elif selected_profile == "Machine Learning Engineer":
        roadmap += [
            "🚀 PHASE 1: ML Engineering Foundations",
            *[f"→ Strengthen {s}" for s in HIGH],
            "→ Review statistics, linear algebra, and probability deeply",
            "→ Master Python: OOP, decorators, generators, async programming",
            "\n🔥 PHASE 2: Model Building & Optimization",
            "→ Build scalable ML models with Scikit-learn, XGBoost, LightGBM",
            "→ Deep learning with PyTorch: build CNNs and Transformers from scratch",
            "→ Master hyperparameter tuning: Optuna, Hyperopt, grid search",
            "→ Learn experiment tracking: MLflow, Weights & Biases",
            "\n💡 PHASE 3: Production & Deployment",
            "→ Containerize models with Docker, orchestrate with Kubernetes",
            "→ Build REST APIs for model serving (FastAPI + Pydantic)",
            "→ Deploy on AWS SageMaker or GCP Vertex AI",
            "→ Learn feature stores: Feast or Tecton",
            "\n🏆 PHASE 4: MLOps & Advanced",
            "→ Build a full MLOps pipeline: data versioning (DVC) → training → CI/CD → monitoring",
            "→ Learn model monitoring and drift detection (Evidently AI, Seldon)",
            "→ Contribute to open-source ML projects on GitHub",
            "→ Target certifications: AWS ML Specialty / GCP Professional ML Engineer",
        ]

    # ---------------- AI ENGINEER ----------------
    elif selected_profile == "AI Engineer":
        roadmap += [
            "🚀 PHASE 1: Core AI & LLM Skills",
            *[f"→ Master {s}" for s in HIGH],
            "→ Deep dive into Transformer architecture (Attention is All You Need paper)",
            "→ Learn the full Hugging Face ecosystem: transformers, datasets, PEFT",
            "\n🔥 PHASE 2: LLM Application Development",
            "→ Build RAG pipelines using LangChain or LlamaIndex",
            "→ Master prompt engineering: chain-of-thought, few-shot, ReAct, tool use",
            "→ Integrate vector databases: Pinecone, Weaviate, or ChromaDB",
            "→ Build an end-to-end AI chatbot with memory and retrieval",
            "\n💡 PHASE 3: Fine-tuning & Production AI",
            "→ Fine-tune open-source LLMs using LoRA / QLoRA (Llama 3, Mistral)",
            "→ Build multi-agent systems using LangGraph or AutoGen",
            "→ Deploy AI APIs on cloud (AWS Lambda, GCP Cloud Run, Modal)",
            "→ Learn AI evaluation: RAGAS, LM-Eval, human preference scoring",
            "\n🏆 PHASE 4: Portfolio & Community",
            "→ Publish an AI project on GitHub (chatbot, RAG app, agent system)",
            "→ Write technical blogs on Towards Data Science or Substack",
            "→ Contribute to Hugging Face open-source repos",
            "→ Target: DeepLearning.AI LangChain specialization, AWS Certified ML",
        ]

    # ---------------- SOFTWARE ENGINEER ----------------
    elif selected_profile == "Software Engineer":
        roadmap += [
            "🚀 PHASE 1: Core CS Fundamentals",
            *[f"→ Strengthen {s}" for s in HIGH],
            "→ Master DSA: arrays, linked lists, trees, graphs, heaps, hashmaps",
            "→ Learn Big-O complexity analysis deeply",
            "\n🔥 PHASE 2: DSA Problem Solving",
            "→ Solve 200+ LeetCode problems — focus on patterns not memorization",
            "→ Key patterns: Two Pointers, Sliding Window, BFS/DFS, Dynamic Programming",
            "→ Practice mock interviews on Pramp, Interviewing.io, or NeetCode",
            "→ Build strong understanding of OOP + SOLID design principles",
            "\n💡 PHASE 3: System Design & Development",
            "→ Learn system design: CAP theorem, sharding, consistent hashing, load balancing",
            "→ Build a backend service with REST APIs (Node.js or Python + FastAPI)",
            "→ Learn databases deeply: SQL query optimization, indexing, transactions",
            "→ Master Git workflows: branching, PR reviews, merge conflicts",
            "\n🏆 PHASE 4: Placement Ready",
            "→ Do 3–5 mock FAANG-style technical interviews",
            "→ Contribute to open-source projects on GitHub (minimum 3 PRs merged)",
            "→ Build a GitHub profile that shows green commit history",
            "→ Prepare behavioral answers using STAR method for leadership stories",
        ]

    # ---------------- BACKEND DEVELOPER ----------------
    elif selected_profile == "Backend Developer":
        roadmap += [
            "🚀 PHASE 1: Backend Fundamentals",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Master HTTP protocol: request lifecycle, status codes, headers, REST principles",
            "→ SQL deep dive: JOINs, indexing, transactions, stored procedures",
            "\n🔥 PHASE 2: API Development",
            "→ Build production-ready REST APIs with Node.js/Express or Python/FastAPI",
            "→ Implement JWT + OAuth2 authentication and role-based authorization",
            "→ Integrate NoSQL databases: MongoDB or Redis for caching",
            "→ Learn message queues: RabbitMQ or Kafka for async processing",
            "\n💡 PHASE 3: Scaling & Architecture",
            "→ Learn microservices architecture vs monolith trade-offs",
            "→ Implement caching strategies (Redis, CDN, cache invalidation patterns)",
            "→ Study system design: load balancers, horizontal vs vertical scaling",
            "→ Containerize apps with Docker and deploy on cloud (AWS EC2/RDS)",
            "\n🏆 PHASE 4: Production Engineering",
            "→ Set up CI/CD pipelines with GitHub Actions or Jenkins",
            "→ Add logging (Winston/Pino) and monitoring (Prometheus + Grafana)",
            "→ Write integration and unit tests (pytest, Jest) — aim for 80%+ coverage",
            "→ Target certifications: AWS Developer Associate / Node.js certifications",
        ]

    # ---------------- FRONTEND DEVELOPER ----------------
    elif selected_profile == "Frontend Developer":
        roadmap += [
            "🚀 PHASE 1: Core Web Fundamentals",
            *[f"→ Master {s}" for s in HIGH],
            "→ HTML5 semantics, forms, accessibility (ARIA roles, WCAG basics)",
            "→ CSS mastery: Flexbox, CSS Grid, animations, custom properties",
            "\n🔥 PHASE 2: JavaScript & Frameworks",
            "→ JavaScript ES6+: closures, promises, async/await, destructuring, modules",
            "→ React.js deep dive: hooks, context API, performance optimization",
            "→ Learn Next.js: SSR, SSG, ISR, App Router, Server Components",
            "→ State management: Redux Toolkit or Zustand",
            "\n💡 PHASE 3: Advanced Frontend",
            "→ TypeScript: interfaces, generics, utility types — adopt in every project",
            "→ Performance: Core Web Vitals, lazy loading, code splitting, bundle analysis",
            "→ Testing: Jest + React Testing Library, Cypress for E2E tests",
            "→ Build tools: Vite, Webpack basics, Babel configuration",
            "\n🏆 PHASE 4: Portfolio & Deployment",
            "→ Build 3 projects: a SaaS landing page, a dashboard, and a full CRUD app",
            "→ Deploy on Vercel or Netlify with CI/CD from GitHub",
            "→ Write Storybook documentation for your component library",
            "→ Contribute to open-source React/Next.js projects",
        ]

    # ---------------- FULL STACK DEVELOPER ----------------
    elif selected_profile == "Full Stack Developer":
        roadmap += [
            "🚀 PHASE 1: Frontend + Backend Foundations",
            *[f"→ Learn {s}" for s in HIGH],
            "→ HTML/CSS/JS fundamentals → React.js with hooks",
            "→ Node.js + Express: routing, middleware, error handling",
            "\n🔥 PHASE 2: Full Integration",
            "→ Build a full-stack CRUD app: React frontend + Node.js/Express backend",
            "→ Connect to PostgreSQL using Prisma or Sequelize ORM",
            "→ Implement JWT authentication (login, refresh tokens, protected routes)",
            "→ REST API design best practices + input validation with Zod/Yup",
            "\n💡 PHASE 3: Database, Auth & Advanced Features",
            "→ Learn database design: normalization, ER diagrams, indexing",
            "→ Integrate file uploads (AWS S3 or Cloudinary)",
            "→ Add real-time features using WebSockets (Socket.io)",
            "→ Learn Next.js for SSR and API routes in a unified codebase",
            "\n🏆 PHASE 4: Deployment & Scale",
            "→ Containerize with Docker + deploy on AWS EC2 or Railway",
            "→ Set up CI/CD via GitHub Actions (lint → test → deploy)",
            "→ Build a portfolio with 2–3 full-stack projects (SaaS clone, marketplace)",
            "→ Target: AWS Cloud Practitioner or Meta Full Stack certification",
        ]

    # ---------------- DEVOPS ENGINEER ----------------
    elif selected_profile == "DevOps Engineer":
        roadmap += [
            "🚀 PHASE 1: Linux & Scripting Basics",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Linux mastery: file system, permissions, process management, cron jobs",
            "→ Bash scripting: loops, functions, pipelines, cron automation",
            "\n🔥 PHASE 2: CI/CD & Containerization",
            "→ Build CI/CD pipelines with GitHub Actions and Jenkins",
            "→ Dockerize multi-service applications (Dockerfile + Docker Compose)",
            "→ Implement blue-green and canary deployment strategies",
            "→ Learn Infrastructure as Code: Terraform (provision cloud resources)",
            "\n💡 PHASE 3: Kubernetes & Orchestration",
            "→ Kubernetes core: Pods, Deployments, Services, ConfigMaps, Secrets",
            "→ Helm charts for templating K8s manifests",
            "→ Set up monitoring with Prometheus + Grafana dashboards",
            "→ Logging stack: ELK (Elasticsearch, Logstash, Kibana) or Loki",
            "\n🏆 PHASE 4: Cloud & Security",
            "→ Deploy production workloads on AWS EKS or GCP GKE",
            "→ Learn DevSecOps: SonarQube, Vault for secrets management",
            "→ Implement GitOps workflow using ArgoCD",
            "→ Target certifications: CKA (Certified Kubernetes Administrator) + AWS DevOps Professional",
        ]

    # ---------------- CLOUD ENGINEER ----------------
    elif selected_profile == "Cloud Engineer":
        roadmap += [
            "🚀 PHASE 1: Cloud Fundamentals",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Understand core cloud concepts: IaaS, PaaS, SaaS, shared responsibility model",
            "→ AWS foundations: EC2, S3, IAM, VPC, RDS, Lambda",
            "\n🔥 PHASE 2: Core Cloud Services",
            "→ Compute, storage, and networking deep dives (Auto Scaling, Route 53, CloudFront)",
            "→ Managed database services: RDS, Aurora, DynamoDB, ElastiCache",
            "→ Serverless architecture: Lambda + API Gateway + DynamoDB pattern",
            "→ Learn Terraform: provision and manage cloud infrastructure as code",
            "\n💡 PHASE 3: Architecture & Security",
            "→ Design highly available, fault-tolerant architectures (multi-AZ, multi-region)",
            "→ Cloud security: IAM least privilege, KMS encryption, security groups, WAF",
            "→ Cost optimization: Reserved Instances, Savings Plans, Spot Instances, FinOps",
            "→ Kubernetes on cloud: EKS (AWS) or GKE (GCP)",
            "\n🏆 PHASE 4: Certifications & Portfolio",
            "→ Target AWS Solutions Architect Associate (SAA-C03) first",
            "→ Then progress to: AWS DevOps Pro or GCP Professional Cloud Architect",
            "→ Build a 3-tier cloud architecture project and document it on GitHub",
            "→ Create a cloud cost optimization case study for your resume",
        ]

    # ---------------- CYBERSECURITY ANALYST ----------------
    elif selected_profile == "Cybersecurity Analyst":
        roadmap += [
            "🚀 PHASE 1: Security Fundamentals",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Networking deep dive: TCP/IP, DNS, HTTP, firewalls, VPNs, subnetting",
            "→ Operating systems security: Linux hardening, Windows AD, file permissions",
            "\n🔥 PHASE 2: Offensive & Defensive Tools",
            "→ Set up a home lab: Kali Linux + VirtualBox/VMware",
            "→ Learn Wireshark for packet analysis, Nmap for network scanning",
            "→ Practice with Metasploit and Burp Suite for penetration testing basics",
            "→ Understand SIEM platforms: Splunk or Microsoft Sentinel for log analysis",
            "\n💡 PHASE 3: Specialized Practice",
            "→ Solve 20+ CTF (Capture The Flag) challenges on HackTheBox or TryHackMe",
            "→ Learn MITRE ATT&CK framework: TTPs, threat hunting, detection engineering",
            "→ Study incident response playbooks and digital forensics (Volatility, Autopsy)",
            "→ Learn cloud security (AWS IAM misconfigurations, CSPM tools)",
            "\n🏆 PHASE 4: Certifications & Career",
            "→ Start with CompTIA Security+ for foundational validation",
            "→ Progress to CEH (Certified Ethical Hacker) or eJPT for offensive skills",
            "→ Aim for OSCP for the gold standard penetration testing certification",
            "→ Participate in bug bounty programs (HackerOne, Bugcrowd) to earn and build reputation",
        ]

    # ---------------- PRODUCT MANAGER ----------------
    elif selected_profile == "Product Manager":
        roadmap += [
            "🚀 PHASE 1: PM Fundamentals",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Study core PM frameworks: Jobs-to-be-Done, Kano model, OKRs, RICE prioritization",
            "→ Read: Inspired (Marty Cagan), Hooked (Nir Eyal), The Lean Startup",
            "\n🔥 PHASE 2: Strategy & Discovery",
            "→ Conduct 10+ user interviews using the Jobs-to-be-Done method",
            "→ Build product roadmaps (Now / Next / Later framework)",
            "→ Write professional PRDs and user stories with clear acceptance criteria",
            "→ Competitive analysis: benchmark 5 competitor products across key metrics",
            "\n💡 PHASE 3: Execution & Metrics",
            "→ Work through the full Agile Scrum cycle: backlog grooming, sprint planning, retrospectives",
            "→ Learn product analytics: set up Mixpanel or Amplitude, define DAU/MAU/retention metrics",
            "→ Run A/B experiments: define hypothesis, sample size, success metrics",
            "→ Wireframe solutions in Figma (low-fidelity is sufficient for PMs)",
            "\n🏆 PHASE 4: Portfolio & Positioning",
            "→ Build a PM portfolio: 2 case studies (problem → discovery → solution → metrics)",
            "→ Solve 20 PM interview questions: estimation, product design, metrics analysis",
            "→ Target: Google PM Certificate, AIPMM CPM, or Reforge Growth Series",
            "→ Network on LinkedIn with PMs from product-led companies (Figma, Notion, Linear)",
        ]

    # ---------------- BUSINESS ANALYST ----------------
    elif selected_profile == "Business Analyst":
        roadmap += [
            "🚀 PHASE 1: BA Core Skills",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Master SQL: complex queries, window functions, CTEs for data extraction",
            "→ Excel advanced: Power Query, Pivot Tables, INDEX/MATCH, scenario modeling",
            "\n🔥 PHASE 2: Analysis & Documentation",
            "→ Business process modeling: BPMN 2.0, As-Is vs To-Be process flows",
            "→ Write professional BRDs and FRDs with clear requirements",
            "→ Conduct gap analysis and root cause analysis (5 Whys, Fishbone diagrams)",
            "→ Build dashboards in Power BI or Tableau for stakeholder reporting",
            "\n💡 PHASE 3: Tools & Collaboration",
            "→ Learn Agile BA: write user stories, manage backlog in Jira/Confluence",
            "→ UAT: write test cases, execute testing, manage defect lifecycle",
            "→ ERP basics: SAP or Salesforce fundamentals for enterprise context",
            "→ Financial modeling: ROI analysis, cost-benefit analysis in Excel",
            "\n🏆 PHASE 4: Certification & Portfolio",
            "→ Target ECBA (Entry Certificate in Business Analysis) from IIBA",
            "→ Build portfolio: 2 BA case studies with process flows and requirements docs",
            "→ Practice behavioral interviews using STAR method for business impact stories",
            "→ Target certifications: PMI-PBA or Agile Analysis Certification (AAC)",
        ]

    # ---------------- UI/UX DESIGNER ----------------
    elif selected_profile == "UI/UX Designer":
        roadmap += [
            "🚀 PHASE 1: Design Foundations",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Visual design principles: typography hierarchy, color theory, whitespace, grid systems",
            "→ Figma deep dive: Auto Layout, components, variants, design tokens",
            "\n🔥 PHASE 2: UX Research & Process",
            "→ Conduct 5 user interviews and synthesize findings with affinity mapping",
            "→ Create user personas, empathy maps, and customer journey maps",
            "→ Information architecture: card sorting, tree testing, sitemap design",
            "→ Wireframe flows in Figma (low-fi → mid-fi → high-fi progression)",
            "\n💡 PHASE 3: Interaction Design & Systems",
            "→ Build an interactive prototype with realistic micro-interactions",
            "→ Run usability tests (3–5 participants minimum) and document findings",
            "→ Create a design system: color palette, typography scale, component library",
            "→ Learn accessibility standards: WCAG 2.1 AA compliance, contrast ratios",
            "\n🏆 PHASE 4: Portfolio & Career",
            "→ Build 3 case studies: each with problem framing, research, design decisions, outcomes",
            "→ Present portfolio on a personal website (Framer, Webflow, or custom site)",
            "→ Learn basic HTML/CSS and Framer Motion to prototype with real interactions",
            "→ Target: Google UX Design Certificate (Coursera) or Interaction Design Foundation courses",
        ]

    # ---------------- MOBILE APP DEVELOPER ----------------
    elif selected_profile == "Mobile App Developer":
        roadmap += [
            "🚀 PHASE 1: Mobile Fundamentals",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Choose your primary stack: Flutter (cross-platform) or Swift/Kotlin (native)",
            "→ Mobile UI basics: navigation patterns, gestures, responsive layouts",
            "\n🔥 PHASE 2: App Development",
            "→ Build a fully functional app: authentication + CRUD + navigation",
            "→ REST API integration: connect to a backend using Retrofit (Android) or Alamofire (iOS)",
            "→ Firebase integration: Auth, Firestore, FCM push notifications",
            "→ State management: BLoC/Riverpod (Flutter) or MVVM (Swift/Kotlin)",
            "\n💡 PHASE 3: Advanced Features",
            "→ Local databases: Room (Android), Core Data (iOS), or SQLite with Drift (Flutter)",
            "→ Performance profiling: memory leaks, frame drop analysis, startup time optimization",
            "→ Deep links, app widgets, and background sync (WorkManager / Background Fetch)",
            "→ Unit testing + UI testing with Espresso (Android) or XCTest (iOS)",
            "\n🏆 PHASE 4: Publish & Portfolio",
            "→ Publish 1 real app on Google Play Store + Apple App Store",
            "→ Set up CI/CD with GitHub Actions + Fastlane for automated builds",
            "→ Document your app architecture (Clean Architecture or MVC/MVVM) on GitHub",
            "→ Target: Google Associate Android Developer or Apple App Development with Swift certification",
        ]

    # ---------------- DEFAULT FALLBACK ----------------
    else:
        roadmap += [
            "🚀 PHASE 1: Learn Missing Skills",
            *[f"→ Learn {s}" for s in HIGH],
            "→ Identify the top 5 skills for your target role and create a learning plan",
            "\n🔥 PHASE 2: Build Projects",
            "→ Build 2–3 hands-on projects that demonstrate your core skills",
            "→ Host all projects on GitHub with clear documentation",
            "\n💡 PHASE 3: Strengthen & Validate",
            "→ Take a recognized online certification for your field",
            "→ Solve domain-specific practice problems (LeetCode, Kaggle, HackTheBox)",
            "\n🏆 PHASE 4: Prepare & Apply",
            "→ Tailor your resume with keywords from job descriptions",
            "→ Practice 20+ behavioral and technical interview questions",
            "→ Apply actively and network on LinkedIn in your target industry",
        ]

    return roadmap