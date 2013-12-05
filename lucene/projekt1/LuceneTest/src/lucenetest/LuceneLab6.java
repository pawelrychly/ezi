package lucenetest;

import java.io.*;
import java.util.*;
import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.*;
import org.apache.lucene.queryParser.*;
import org.apache.lucene.search.*;
import org.apache.lucene.document.*;

public class LuceneLab6 {
	//TODO follows TODOs; there four places that should be filled with code
	//according to the instructions given in Lab6.pdf
	
	//directory where the index would be placed in
	//provided by the user as args[1]; set in main()   
    public static String indexPath;

    //TODO create the index, fill it with documents (use indexDoc function), close the index
    public static void createIndex(String path) throws Exception {
    
    	//System.out.println("I'll will create index, feed it, and close it - still to be implemented");
        IndexWriter writer = new IndexWriter(indexPath, new StandardAnalyzer());
        
        File[] files = new File(path).listFiles();
        for(File f: files) {
            if(f.isFile())
            {
                writer.addDocument(indexDoc(f.getAbsolutePath()));
            }
        }
        writer.close();
    }
    
    //TODO create object of class Document; create some necessary fields (e.g. path, content)
    //call this function in createIndex() to create Documents that would be subsequently added to the index
    public static Document indexDoc(String docPath) throws Exception {
		Document d = new Document();
                d.add(new Field("path", docPath, Field.Store.YES, Field.Index.TOKENIZED));
                d.add(new Field("content", new FileReader(docPath)));
		return d;
    }

    //TODO create objects of class: Analyzer, IndexSearcher, QueryParser, Query and Hits
    //for Analyzer remember to use the same constructor as for IndexWriter
    //for QueryParser indicate the fields to be analyzed
    //for Query you should parse "queryString" which is given as a parameter of the function
    //for Hits you should search results for a given query and return them
    public static Hits processQuery(String queryString) throws IOException, ParseException {
	IndexSearcher isearch = new IndexSearcher(indexPath); 
        QueryParser qparser = new QueryParser("content", new StandardAnalyzer()); 

        Query query = qparser.parse(queryString); 
        Hits hits = isearch.search(query); 
	return hits;
    }
    
    public static void main(String [] args) {
		if (args.length < 2) {
		    System.out.println("java -cp lucene-core-2.2.0.jar:. BasicIRsystem texts_path index_path");
		    System.out.println("need two args with paths to the collection of texts and to the directory where the index would be stored, respectively");
		    System.exit(1);
		}
		try {
		    String textsPath = args[0];
		    indexPath = args[1];
		    createIndex(textsPath);
		    String query = " ";

		    //process queries until one writes "lab6"
		    while (true) {
				Scanner sc = new Scanner(System.in);
				System.out.println("Please enter your query: (lab9 to quit)");
				query = sc.next();
				
				if (query.equals("lab9")) {break;} //to quit
					
				Hits hits = processQuery(query);
				
				if (hits != null)
				{
					System.out.println(hits.length() + " result(s) found");
				
					Iterator iter = hits.iterator();
					while(iter.hasNext()){
					    Hit hit = (Hit) iter.next();
					    
					    try {
					    
					    	System.out.println(hit.get("path") + " : " + hit.getScore());
                                                //TODO get the Document that matches query
					    	//read off and write its name and similarity score to the Console
											    
					    }
					    catch (Exception e) {
					    	System.err.println("Unexpected exception");
					    	System.err.println(e.toString());
					    }
					}
				}
				else
				{
					System.out.println("Processing the query still not implemented, heh?");
				}
		    }
		    
		} catch (Exception e) {
		    System.err.println("Even more unexpected exception");
		    System.err.println(e.toString());
		}   
    }
}
