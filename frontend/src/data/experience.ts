export interface Experience {
  id: string;
  period: string;
  company: string;
  role: string;
  startMonth: string;
  endMonth: string;
  ongoing: boolean;
  bullets: string[];
}

export const experienceData: Experience[] = [
  {
    id: "1",
    period: "2026-Present",
    company: "Islamic Relief Afghanistan",
    role: "Freelancing & AI Trainer",
    startMonth: "Feb 2026",
    endMonth: "Present",
    ongoing: true,
    bullets: [
      "Delivered practical training on freelancing, remote work, AI tools, and digital service building.",
      "Taught learners how to use AI for workflow automation, content generation, productivity, and client project delivery.",
      "Guided trainees in building AI-powered digital services, online portfolios, and automation-based solutions.",
      "Provided hands-on training with Zapier, Make, n8n, API integrations, and automation pipelines."
    ]
  },
  {
    id: "2",
    period: "2020-Present",
    company: "Freelance / Remote",
    role: "Data Analyst & Machine Learning Engineer",
    startMonth: "2020",
    endMonth: "Present",
    ongoing: true,
    bullets: [
      "Completed data analysis and visualization projects using Python, Pandas, Matplotlib, Power BI, and Tableau.",
      "Developed machine learning models for prediction, classification, and clustering tasks.",
      "Provided AI/ML consultation and technical support for international clients.",
      "Built dashboards, reports, and automation-based solutions for client projects."
    ]
  },
  {
    id: "3",
    period: "2025",
    company: "UNDP",
    role: "AI / ML Trainer",
    startMonth: "Jul 2025",
    endMonth: "Sep 2025",
    ongoing: false,
    bullets: [
      "Delivered AI and machine learning training sessions for capacity-building programs.",
      "Designed practical AI/ML examples using Python, SQL, and automation frameworks.",
      "Built and fine-tuned predictive models for real-world use cases, including classification and time-series forecasting.",
      "Developed data analytics pipelines and dashboards for tracking educational impact and insights."
    ]
  },
  {
    id: "4",
    period: "2024-2025",
    company: "Ghazi Amanullah Khan University",
    role: "Visiting Lecturer & AI/Python Trainer",
    startMonth: "Mar 2024",
    endMonth: "Apr 2025",
    ongoing: false,
    bullets: [
      "Delivered lectures and practical sessions in Artificial Intelligence, Python Programming, IT, and Web Development.",
      "Designed hands-on learning activities for undergraduate students and trainees.",
      "Simplified complex AI, programming, and technology topics for beginner and intermediate learners."
    ]
  },
  {
    id: "5",
    period: "2021-2024",
    company: "AMHTC",
    role: "System Manager / Data & Automation Systems Developer",
    startMonth: "2021",
    endMonth: "Jan 2024",
    ongoing: false,
    bullets: [
      "Designed and managed backend systems for internal data processing and operational tools using Python and SQL.",
      "Developed forecasting models to support business planning and data-driven decision-making.",
      "Built data analytics pipelines for real-time reporting and business intelligence.",
      "Automated internal workflows by improving system inputs, outputs, and reporting processes."
    ]
  },
  {
    id: "6",
    period: "2020-2021",
    company: "IO Global Services Pvt. Ltd.",
    role: "Field Engineer / Technical Assistant",
    startMonth: "Feb 2020",
    endMonth: "Mar 2021",
    ongoing: false,
    bullets: [
      "Provided technical support for hardware, networking, and field-level systems.",
      "Assisted with system installation, maintenance, diagnostics, and troubleshooting.",
      "Supported operational teams in improving infrastructure reliability and resolving technical issues."
    ]
  }
];
