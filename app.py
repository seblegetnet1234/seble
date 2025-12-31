from flask import Flask, render_template, request, jsonify
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_processor import AmharicMedicalDataProcessor
from src.indexer import AmharicMedicalIndexer
from src.evaluator import IRSystemEvaluator, TestQueryGenerator

app = Flask(__name__)

# Global variables for system components
processor = None
indexer = None
evaluator = None
documents = []

def initialize_system():
    """Initialize the IR system with sample data"""
    global processor, indexer, evaluator, documents
    
    print("Initializing Amharic Medical IR System...")
    
    # Initialize components
    processor = AmharicMedicalDataProcessor()
    indexer = AmharicMedicalIndexer("index")
    evaluator = IRSystemEvaluator()
    
    # Sample CSV data
    csv_data = """title_am,generic_name_am,category_am,symptom_am,usage_am,side_effects_am,contraindications_am,dosage_am,manufacturer_am,availability_am,price
ቪታሚን C,Vit C,የሆድ መድሃኒት,ቁርጠት,በቀን 2 ጊዜ,ተኩስ,እርጉዝ ሴቶች,250mg,SinoMed,አልተገኘም,156.52
ፓራሲታሞል,Paracetamol,አናልጀዝክ,ህመም,ከመብላት በኋላ,ራስ ምታት,የደም ግፊት ችግር,5ml,Julphar,ተገኝቷል,160.85
አሞክሲሲሊን,Amoxicillin,አንቲባዮቲክ,ኢንፌክሽን,በቀን 3 ጊዜ,,የልብ ችግኝ,250mg,Addis Pharma,ተገኝቷል,94.31
መትፎርሚን,Metformin,የስኳር መድሃኒት,ህመም,ከመብላት በኋላ,,የደም ግፊት ችግር,100mg,Julphar,አልተገኘም,177.02
አስፒሪን,Aspirin,ቫይታሚን,ማቅለሽለሽ,ከመብላት በፊት,ተኩስ,የደም ግፊት ችግር,100mg,Cadila,ተገኝቷል,46.35
ሎራቲዲን,Loratadine,የስኳር መድሃኒት,ኢንፌክሽን,በቀን 2 ጊዜ,ተኩስ,የደም ግፊት ችግኝ,5ml,Julphar,ተገኝቷል,125.68
ሴፋሌክሲን,Cephalexin,የስኳር መድሃኒት,እርፍት,ከመብላት በፊት,ማቅለሽለሽ,እርጉዝ ሴቶች,100mg,SinoMed,አልተገኘም,16.64
ኢቡፕሮፈን,Ibuprofen,የስኳር መድሃኒት,እርፍት,ከመብላት በፊት,,የደም ግፊት ችግር,5ml,Addis Pharma,ተገኝቷል,35.89
ኦሜፕራዞል,Omeprazole,አናልጀዝክ,ማቅለሽለሽ,ከመብላት በፊት,ማቅለሽለሽ,እርጉዝ ሴቶች,100mg,SinoMed,አልተገኘም,133.12
አዚትሮማይሲን,Azithromycin,አንቲባዮቲክ,ትኩሳት,ከመብላት በኋላ,ተኩስ,የደም ግፊት ችግኝ,10ml,Humanwell,ተገኝቷል,96.56"""
    
    # Process documents
    documents, df = processor.create_document_collection(csv_data)
    
    # Create index
    indexer.add_documents(documents)
    
    print(f"System initialized with {len(documents)} documents")

@app.route('/')
def home():
    """Home page with search interface"""
    initialize_system()
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle search requests"""
    initialize_system()
    
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        limit = int(request.form.get('limit', 10))
    else:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 10))
    
    if not query:
        return render_template('search_results.html', 
                             query='', 
                             results=[], 
                             message='እባክዎ የፍለጋ ቃል ያስገቡ (Please enter a search term)')
    
    # Perform search
    results = indexer.search(query, limit=limit)
    
    # Prepare results for display
    search_results = []
    for result in results:
        search_results.append({
            'id': result['id'],
            'title': result['title'],
            'content': result['content'][:200] + '...' if len(result['content']) > 200 else result['content'],
            'category': result['category'],
            'score': round(result['score'], 3),
            'rank': result['rank']
        })
    
    message = f"{len(results)} ውጤቶች ተገኝተዋል ({len(results)} results found)" if results else "ምንም ውጤት አልተገኘም (No results found)"
    
    return render_template('search_results.html', 
                         query=query, 
                         results=search_results, 
                         message=message)

@app.route('/document/<doc_id>')
def view_document(doc_id):
    """View full document details"""
    initialize_system()
    
    # Find document by ID
    document = None
    for doc in documents:
        if doc['id'] == doc_id:
            document = doc
            break
    
    if not document:
        return "Document not found", 404
    
    return render_template('document.html', document=document)

@app.route('/statistics')
def statistics():
    """Show system statistics"""
    initialize_system()
    
    # Get document statistics
    doc_stats = processor.get_document_statistics(documents)
    
    # Get index statistics
    index_stats = indexer.get_index_statistics()
    
    # Category distribution
    category_counts = {}
    for doc in documents:
        category = doc.get('category_am', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    stats = {
        'document_stats': doc_stats,
        'index_stats': index_stats,
        'category_distribution': category_counts
    }
    
    return render_template('statistics.html', stats=stats)

@app.route('/api/search')
def api_search():
    """API endpoint for search"""
    initialize_system()
    
    query = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = indexer.search(query, limit=limit)
    
    return jsonify({
        'query': query,
        'results': results,
        'total': len(results)
    })

if __name__ == '__main__':
    initialize_system()
    app.run(debug=True, host='127.0.0.1', port=8000, use_reloader=False)