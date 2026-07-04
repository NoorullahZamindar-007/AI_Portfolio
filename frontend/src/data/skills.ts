export interface SkillCategory {
  title: string;
  description: string;
  icon: string;
  skills: string[];
  color: string;
}

export const skillsData: SkillCategory[] = [
  {
    title: "Programming & Data Science",
    description: "Working with Python and data science libraries to clean, analyze, model, and visualize data.",
    icon: "Code",
    skills: ["Python", "Pandas", "NumPy", "SciPy", "Matplotlib", "Scikit-learn"],
    color: "bg-indigo-50 border-indigo-100 text-indigo-700"
  },
  {
    title: "Machine Learning & Deep Learning",
    description: "Building classification, regression, clustering, forecasting, and neural network models.",
    icon: "Brain",
    skills: ["TensorFlow", "Keras", "Classification", "Regression", "Clustering", "Forecasting"],
    color: "bg-violet-50 border-violet-100 text-violet-700"
  },
  {
    title: "AI Engineering & Automation",
    description: "Designing AI agents, automation pipelines, and API-based intelligent workflows.",
    icon: "Workflow",
    skills: ["AI Agents", "RAG Concepts", "LLM APIs", "Zapier", "Make", "n8n", "Webhooks", "JSON Automation"],
    color: "bg-emerald-50 border-emerald-100 text-emerald-700"
  },
  {
    title: "Backend & Web",
    description: "Creating web applications, APIs, and practical backend systems.",
    icon: "Server",
    skills: ["Flask", "REST APIs", "HTML", "CSS", "Bootstrap", "Tailwind CSS"],
    color: "bg-sky-50 border-sky-100 text-sky-700"
  },
  {
    title: "Databases & Visualization",
    description: "Managing databases and building dashboards for reporting and business insight.",
    icon: "Database",
    skills: ["MySQL", "SQL Server", "SQLite", "Power BI", "Tableau", "Dashboards", "Reporting"],
    color: "bg-amber-50 border-amber-100 text-amber-700"
  },
  {
    title: "Tools & Collaboration",
    description: "Using modern development tools for research, documentation, experiments, and delivery.",
    icon: "Tool",
    skills: ["Git", "GitHub", "VS Code", "Anaconda", "Google Colab", "Documentation", "Teaching"],
    color: "bg-rose-50 border-rose-100 text-rose-700"
  }
];
