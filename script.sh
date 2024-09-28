
#!/bin/bash
case $1 in 
    app)
        echo "Running App"
        python app.py
        ;;
    test)
        echo "Running Tests"
        python -m unittests
        ;;
    clear)
        echo "Deleting generated files from repo"
        rm expiring_or_expired.json fiscal_year_completions.json training_counts.json
esac
        