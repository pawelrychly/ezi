/*
 * Skeleton class for the Lucene search program implementation
 */
package lucenebbc;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.Field.Store;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexableField;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.BooleanClause;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TermRangeQuery;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;

public class LuceneSearchApp {
	
	public LuceneSearchApp() {

	}
	Directory index = new RAMDirectory();
        StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_41);
            
	public void index(List<RssFeedDocument> docs) {
                // implement the Lucene indexing here
            IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_41, analyzer);
            IndexWriter w = null;
            try {
                w = new IndexWriter(index, config);
                SimpleDateFormat dt = new SimpleDateFormat("yyyy-MM-dd"); 

                for(RssFeedDocument doc: docs) {
                    Document d = new Document();
                    d.add(new TextField("title", doc.getTitle(), Store.YES));
                    d.add(new TextField("pubdate", dt.format(doc.getPubDate()).replace("-", ""), Store.YES));
                    d.add(new TextField("description", doc.getDescription(), Store.YES));
                    w.addDocument(d);
                }
                w.close();
            } catch (IOException ex) {
                Logger.getLogger(LuceneSearchApp.class.getName()).log(Level.SEVERE, null, ex);
            }
	}
	
	public List<String> search(List<String> inTitle, List<String> notInTitle, List<String> inDescription, List<String> notInDescription, String startDate, String endDate) {
		
		printQuery(inTitle, notInTitle, inDescription, notInDescription, startDate, endDate);

		List<String> results = new LinkedList<String>();
                BooleanQuery bq = new BooleanQuery();
                if(inTitle != null) {
                    for(String s: inTitle) {
                        bq.add(new TermQuery(new Term("title", s)), BooleanClause.Occur.MUST);
                    }
                }
                if(notInTitle != null) {
                    for(String s: notInTitle) {
                        bq.add(new TermQuery(new Term("title", s)), BooleanClause.Occur.MUST_NOT);
                    }
                }
                if(inDescription != null) {
                    for(String s: inDescription) {
                        bq.add(new TermQuery(new Term("description", s)), BooleanClause.Occur.MUST);
                    }
                }
                if(notInDescription != null) {
                    for(String s: notInDescription) {
                        bq.add(new TermQuery(new Term("description", s)), BooleanClause.Occur.MUST_NOT);
                    }
                }
                
                
                if(startDate != null || endDate != null) {
                    boolean addStart = startDate != null ? true : false;
                    boolean addEnd = endDate != null ? true : false;
                    if(addStart) {
                        startDate = startDate.replace("-", "");
                    }
                    if(addEnd) {
                        endDate = endDate.replace("-", "");
                    }
                    bq.add(TermRangeQuery.newStringRange("pubdate", startDate, endDate, addStart, addEnd), BooleanClause.Occur.MUST);
                }
                
                
                //date
                
               IndexReader reader = null;
            try {
                reader = DirectoryReader.open(index);
                IndexSearcher searcher = new IndexSearcher(reader);
                TopDocs result = searcher.search(bq, 1000);
                ScoreDoc[] sd = result.scoreDocs;

                for(int i=0; i<sd.length; i++) {
                    Document doc = searcher.doc(sd[i].doc);
                    results.add(doc.getField("title").stringValue());
                }

            } catch (IOException ex) {
                Logger.getLogger(LuceneSearchApp.class.getName()).log(Level.SEVERE, null, ex);
            }

                
                
		
		return results;
	}
	
	public void printQuery(List<String> inTitle, List<String> notInTitle, List<String> inDescription, List<String> notInDescription, String startDate, String endDate) {
		System.out.print("Search (");
		if (inTitle != null) {
			System.out.print("in title: "+inTitle);
			if (notInTitle != null || inDescription != null || notInDescription != null || startDate != null || endDate != null)
				System.out.print("; ");
		}
		if (notInTitle != null) {
			System.out.print("not in title: "+notInTitle);
			if (inDescription != null || notInDescription != null || startDate != null || endDate != null)
				System.out.print("; ");
		}
		if (inDescription != null) {
			System.out.print("in description: "+inDescription);
			if (notInDescription != null || startDate != null || endDate != null)
				System.out.print("; ");
		}
		if (notInDescription != null) {
			System.out.print("not in description: "+notInDescription);
			if (startDate != null || endDate != null)
				System.out.print("; ");
		}
		if (startDate != null) {
			System.out.print("startDate: "+startDate);
			if (endDate != null)
				System.out.print("; ");
		}
		if (endDate != null)
			System.out.print("endDate: "+endDate);
		System.out.println("):");
	}
	
	public void printResults(List<String> results) {
		if (results.size() > 0) {
			Collections.sort(results);
			for (int i=0; i<results.size(); i++)
				System.out.println(" " + (i+1) + ". " + results.get(i));
		}
		else
			System.out.println(" no results");
	}
	
	public static void main(String[] args) {
		if (args.length > 0) {
			LuceneSearchApp engine = new LuceneSearchApp();
			
			RssFeedParser parser = new RssFeedParser();
			parser.parse(args[0]);
			List<RssFeedDocument> docs = parser.getDocuments();
			
			engine.index(docs);

			List<String> inTitle;
			List<String> notInTitle;
			List<String> inDescription;
			List<String> notInDescription;
			List<String> results;
			
			// 1) search documents with words "kim" and "korea" in the title
			inTitle = new LinkedList<String>();
			inTitle.add("kim");
			inTitle.add("korea");
			results = engine.search(inTitle, null, null, null, null, null);
			engine.printResults(results);
			
			// 2) search documents with word "kim" in the title and no word "korea" in the description
			inTitle = new LinkedList<String>();
			notInDescription = new LinkedList<String>();
			inTitle.add("kim");
			notInDescription.add("korea");
			results = engine.search(inTitle, null, null, notInDescription, null, null);
			engine.printResults(results);

			// 3) search documents with word "us" in the title, no word "dawn" in the title and word "" and "" in the description
			inTitle = new LinkedList<String>();
			inTitle.add("us");
			notInTitle = new LinkedList<String>();
			notInTitle.add("dawn");
			inDescription = new LinkedList<String>();
			inDescription.add("american");
			inDescription.add("confession");
			results = engine.search(inTitle, notInTitle, inDescription, null, null, null);
			engine.printResults(results);
			
			// 4) search documents whose publication date is 2011-12-18
			results = engine.search(null, null, null, null, "2011-12-18", "2011-12-18");
			engine.printResults(results);
			
			// 5) search documents with word "video" in the title whose publication date is 2000-01-01 or later
			inTitle = new LinkedList<String>();
			inTitle.add("video");
			results = engine.search(inTitle, null, null, null, "2000-01-01", null);
			engine.printResults(results);
			
			// 6) search documents with no word "canada" or "iraq" or "israel" in the description whose publication date is 2011-12-18 or earlier
			notInDescription = new LinkedList<String>();
			notInDescription.add("canada");
			notInDescription.add("iraq");
			notInDescription.add("israel");
			results = engine.search(null, null, null, notInDescription, null, "2011-12-18");
			engine.printResults(results);
		}
		else
			System.out.println("ERROR: the path of a RSS Feed file has to be passed as a command line argument.");
	}
}
