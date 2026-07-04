export interface Project {
  id: string;
  category: string;
  title: string;
  thumbnail: string;
  fallbackThumbnail?: string;
  description: string;
  technologies: string[];
  links: { label: string; url: string }[];
  screenshots: string[];
  fallbackScreenshots?: string[];
}

const githubProfile = "https://github.com/NoorullahZamindar-007";
const portfolioUrl = "https://noorullahzamindar-007.github.io/Portfolio/";

export const projectsData: Project[] = [
  {
    id: "1",
    category: "Computer Vision",
    title: "Facial Emotion Recognition System",
    thumbnail: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?q=80&w=900&auto=format&fit=crop",
    description: "An AI-based system that detects human facial emotions from images or video using computer vision and deep learning models.",
    technologies: ["Python", "OpenCV", "TensorFlow", "Keras", "Scikit-learn", "Flask"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "2",
    category: "AI Automation",
    title: "AI Email Auto-Responder Agent",
    thumbnail: "https://images.unsplash.com/photo-1596526131083-e8c633c948d2?q=80&w=900&auto=format&fit=crop",
    description: "An AI-powered email automation agent that reads incoming emails and generates intelligent replies using API integrations and automation workflows.",
    technologies: ["Python", "Gmail API", "LLM APIs", "Automation Workflows", "JSON"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "3",
    category: "Chatbots",
    title: "WhatsApp / Telegram Customer Support Bot",
    thumbnail: "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?q=80&w=900&auto=format&fit=crop",
    description: "An automated customer support chatbot that understands user intent and responds to common questions instantly through messaging platforms.",
    technologies: ["Python", "Intent Detection", "Chatbot Logic", "API Integration", "Automation Tools"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "4",
    category: "Document AI",
    title: "AI Invoice & Document Extractor",
    thumbnail: "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?q=80&w=900&auto=format&fit=crop",
    description: "A business document automation system that extracts important information from invoices and documents using OCR and machine learning.",
    technologies: ["Python", "OCR", "Machine Learning", "Data Extraction", "Automation"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "5",
    category: "Web Application",
    title: "Car Reservation Web Application",
    thumbnail: "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?q=80&w=900&auto=format&fit=crop",
    description: "An online car reservation web application for a USA-based client, including backend logic and frontend user interface.",
    technologies: ["Flask", "Flutter", "Python", "Database", "HTML", "CSS"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "6",
    category: "Generative AI",
    title: "AI Social Media Auto-Post Generator",
    thumbnail: "https://images.unsplash.com/photo-1611162616475-46b635cb6868?q=80&w=900&auto=format&fit=crop",
    description: "An AI-powered tool that generates and schedules social media posts automatically using generative AI and automation workflows.",
    technologies: ["AI Text Generation", "APIs", "Scheduling Workflows", "Automation Tools"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "7",
    category: "Desktop Analytics",
    title: "AI-Enhanced POS Desktop System",
    thumbnail: "https://images.unsplash.com/photo-1556742502-ec7c0e9f34b1?q=80&w=900&auto=format&fit=crop",
    description: "A POS desktop application with AI analytics for sales insights and predictive business reporting.",
    technologies: ["Python", "PyQt6", "SQLite", "Data Analytics", "Predictive Reporting"],
    links: [
      { label: "Portfolio", url: portfolioUrl },
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  }
];
