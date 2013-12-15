/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pagerankinvertedindex;

import ir.utilities.DoubleValue;
import ir.utilities.Weight;
import ir.vsr.DocumentIterator;
import ir.vsr.DocumentReference;
import ir.vsr.HashMapVector;
import ir.vsr.InvertedIndex;
import ir.vsr.Retrieval;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;


public class PageRankInvertedIndex extends InvertedIndex {

    private double weight = 0.0;
    private HashMap<String, Double> pageRanks = new HashMap<String, Double>();

    public PageRankInvertedIndex(File dirFile, short docType, boolean stem, boolean feedback, double weight) {
        super(dirFile, docType, stem, feedback);
        this.weight = weight;
        String dir = dirFile.getPath();
        try {
            FileReader in = new FileReader(new File(dir, "pageRanks.txt"));
            BufferedReader br = new BufferedReader(new FileReader(new File(dir, "pageRanks.txt")));
            String line;
            while ((line = br.readLine()) != null) {
                String[] elements = line.split(" ");
                pageRanks.put(elements[0], Double.parseDouble(elements[1]));
                //System.out.println(elements[0]);
            }
            in.close();

        } catch (IOException e) {
            System.err.println("HTMLPage.writeAbsolute(): " + e);
        }
        dir = dir + "pageRank.txt";
    }

    @Override
    public Retrieval[] retrieve(HashMapVector vector) {
        // Create a hashtable to store the retrieved documents.  Keys
        // are docRefs and values are DoubleValues which indicate the
        // partial score accumulated for this document so far.
        // As each token in the query is processed, each document
        // it indexes is added to this hashtable and its retrieval
        // score (similarity to the query) is appropriately updated.
        HashMap retrievalHash = new HashMap();
        // Initialize a variable to store the length of the query vector
        double queryLength = 0.0;
        // Iterate through each token in the query input Document
        Iterator mapEntries = vector.iterator();
        while (mapEntries.hasNext()) {
            // Get the token and the count for each token in the query
            Map.Entry entry = (Map.Entry) mapEntries.next();
            String token = (String) entry.getKey();
            double count = ((Weight) entry.getValue()).getValue();
            // Determine the score added to the similarity of each document
            // indexed under this token and update the length of the
            // query vector with the square of the weight for this token.
            queryLength = queryLength + incorporateToken(token, count, retrievalHash);
        }
        // Finalize the length of the query vector by taking the square-root of the
        // final sum of squares of its token wieghts.
        queryLength = Math.sqrt(queryLength);
        // Make an array to store the final ranked Retrievals.
        Retrieval[] retrievals = new Retrieval[retrievalHash.size()];
        // Iterate through each of the retreived docuements stored in
        // the final retrievalHash.
        Iterator rmapEntries = retrievalHash.entrySet().iterator();
        int retrievalCount = 0;
        while (rmapEntries.hasNext()) {
            // Get the DocumentReference and score for each retrieved document
            Map.Entry entry = (Map.Entry) rmapEntries.next();
            DocumentReference docRef = (DocumentReference) entry.getKey();
            double score = ((DoubleValue) entry.getValue()).value;
            // Normalize score for the lengths of the two document vectors
            score = score / (queryLength * docRef.length);
            // Add a Retrieval for this document to the result array
            retrievals[retrievalCount++] = new Retrieval(docRef, score);
        }
        
        for (int i = 0; i < retrievals.length; i++) {
            String name = retrievals[i].docRef.file.getName();
            name = name.replace(".html.html", ".html");
            if (pageRanks.containsKey(name)) {
                retrievals[i].score = retrievals[i].score + this.weight * pageRanks.get(name);
            } 
        }
        
        // Sort the retrievals to produce a final ranked list using the
        // Comparator for retrievals that produces a best to worst ordering.
        Arrays.sort(retrievals);
        return retrievals;
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String dirName = args[args.length - 1];
        short docType = DocumentIterator.TYPE_TEXT;
        boolean stem = false, feedback = false;
        double weight = 0.0;
        for (int i = 0; i < args.length - 1; i++) {
            String flag = args[i];
            if (flag.equals("-weight")) // Create HTMLFileDocuments to filter HTML tags
            {
                weight = Double.parseDouble(args[i + 1]);
            }
        }
        // Create an inverted index for the files in the given directory.
        PageRankInvertedIndex index = new PageRankInvertedIndex(new File(dirName), docType, stem, feedback, weight);
        // index.print();
        // Interactively process queries to this index.
        index.processQueries();
    }
}
