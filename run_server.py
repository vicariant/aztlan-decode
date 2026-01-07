# -*- coding: utf-8 -*-
import sys
import os
os.chdir(r'C:\Users\chris\OneDrive\Documentos\aztlan-decode')
if __name__ == '__main__':
    from app import app, initialize_app
    initialize_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
