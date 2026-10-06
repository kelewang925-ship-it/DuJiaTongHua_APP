"""Rerun both real registered-user journeys and the preceding product regressions."""
import subprocess,sys
from verify_pet_controls import ROOT
codes=[subprocess.run([sys.executable,str(ROOT/script)]).returncode for script in ['verify_time_product_journey.py','verify_product_journey.py','verify_product_journey_regressions.py']]
raise SystemExit(0 if all(v==0 for v in codes)else 1)
