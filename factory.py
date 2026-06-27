import sqlite3
import subprocess
import os
import time

DB_PATH = ".commonai/ontology.db"
WORKSPACE_DIR = ".commonai/workspace"
AGENTS_FILE = ".commonai/AGENTS.md"

def get_pending_user_stories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT us.id, f.name, us.role, us.action, us.value 
        FROM user_stories us
        JOIN features f ON us.feature_id = f.id
        WHERE us.status = 'pending'
    """)
    stories = cursor.fetchall()
    conn.close()
    return stories

def get_acceptance_criteria(story_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM acceptance_criteria WHERE user_story_id = ?", (story_id,))
    ac_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ac_list

def run_agent_step(agent_name, prompt, context_data):
    print(f"\n🚀 [EXEC] Triggering {agent_name}...")
    context_file = os.path.join(WORKSPACE_DIR, f"transient_context_{agent_name}.md")
    
    with open(context_file, "w") as f:
        f.write(context_data)
    
    command = (
        f"agy --sandbox \"{prompt}. Read context from {context_file}. "
        f"Adhere to your persona in {AGENTS_FILE}.\" "
        f"--auto-approve"
    )
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ [ERROR] {agent_name} crashed: {result.stderr}")
        return False, result.stderr
        
    if "VALIDATION_FAILED" in result.stdout:
        print(f"⚠️ [REJECTED] {agent_name} flagged an issue.")
        return False, result.stdout
        
    return True, result.stdout

def process_user_story(story):
    story_id, feature_name, role, action, value = story
    print(f"\n" + "="*50)
    print(f"⚙️  PROCESSING STORY {story_id}: As a {role}, I want to {action}")
    print("="*50)
    
    ac_list = get_acceptance_criteria(story_id)
    base_context = f"Feature: {feature_name}\nStory: As a {role}, I want to {action} so that {value}\nAC:\n" + "\n".join([f"- {ac}" for ac in ac_list])
    
    run_agent_step("po-architect", "Refine this story and define exact functional test strategies.", base_context)
    
    is_visual = any(keyword in action.lower() for keyword in ["view", "page", "button", "dashboard", "ui", "screen"])
    if is_visual:
        run_agent_step("ux-designer", "Generate Bootstrap 5 HTML structure for this story based on the global style guide.", base_context)

    max_retries = 3
    attempt = 1
    
    while attempt <= max_retries:
        print(f"\n🔄 --- Implementation Loop (Attempt {attempt}/{max_retries}) ---")
        
        success, out = run_agent_step("tech-architect", "Write TECH_SPEC.md detailing FastAPI routes and Postgres schemas.", base_context)
        success, out = run_agent_step("impl-collection", "Implement the backend, frontend, and database changes defined in TECH_SPEC.md.", "Read TECH_SPEC.md")
        run_agent_step("qa-testers", "Write Pytest and Testcontainers integration tests targeting 80% coverage.", "Read TECH_SPEC.md")
        success, out = run_agent_step("validators", "Review the code and tests. Run Pytest. If tests fail or code has SQL injection risks, output VALIDATION_FAILED.", "Read TECH_SPEC.md")
        
        if success:
            print("✅ Validation passed! Breaking out of loop.")
            break
        else:
            print(f"🔙 Validation failed. Feeding errors back to Architect...")
            base_context += f"\n\nPREVIOUS FAILURE on Attempt {attempt}:\n{out}\nFix these issues in the next architecture spec."
            attempt += 1

    if attempt > max_retries:
        print(f"🚨 Max retries reached for Story {story_id}. Halting for human review.")
        return

    run_agent_step("tech-writer", f"Generate report-{story_id}.md detailing the workflow and test results. Update the CSV.", base_context)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_stories SET status = 'completed' WHERE id = ?", (story_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    stories = get_pending_user_stories()
    
    if not stories:
        print("🎉 No pending stories found in ontology.db.")
    else:
        print("🏗️  Running Sprint Zero: Scaffolding and Dependencies...")
        
        run_agent_step(
            "tech-architect", 
            "Generate and execute the bash script to create the base repository directories.", 
            "Read the project-scaffold skill."
        )
        
        run_agent_step(
            "devops-docker", 
            "Install the Python dependencies required for the project.", 
            "Read the dependency-manager skill. Use the requirements.txt file in the workspace."
        )
        
        for story in stories:
            process_user_story(story)