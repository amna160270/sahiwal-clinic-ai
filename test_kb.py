from knowledge_base import MedicalKnowledgeBase

kb = MedicalKnowledgeBase()
kb.build_db("data/medical.txt")

print(kb.search("fever"))