# Services-Monitoring-Automation
#env setup
python -m venv myenv
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # macOS/Linux
pip install streamlit pandas openpyxl

#Frontend run
streamlit run app.py
