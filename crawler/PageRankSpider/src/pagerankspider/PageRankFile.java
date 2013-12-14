package pagerankspider;

import ir.utilities.MoreMath;
import ir.webutils.Graph;
import ir.webutils.Node;
import ir.webutils.PageRank;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 */
public class PageRankFile {

    
    public static HashMap<String, Double> countPageRank(Graph graph, double alpha, int iterations) {
        Node[] nodes = graph.nodeArray();
        HashMap indexMap = new HashMap((int) 1.4 * nodes.length);
        double[] r = new double[nodes.length];
        double[] rp = new double[nodes.length];
        double[] e = new double[nodes.length];
        for (int i = 0; i < nodes.length; i++) {
            indexMap.put(nodes[i].toString(), new Integer(i));
//	    System.out.print(nodes[i] + " ");
            r[i] = 1.0 / nodes.length;
            e[i] = alpha / nodes.length;
        }
        //System.out.print("\nR = ");
        MoreMath.printVector(r);
        //System.out.print("\nE = ");
        MoreMath.printVector(e);
        for (int j = 0; j < iterations; j++) {
            //System.out.println("\nIteration " + (j+1) + ":");
            for (int i = 0; i < nodes.length; i++) {
                ArrayList inNodes = nodes[i].getEdgesIn();
                rp[i] = 0;
                for (int k = 0; k < inNodes.size(); k++) {
                    Node inNode = (Node) inNodes.get(k);
                    String inName = inNode.toString();
                    int fanOut = inNode.getEdgesOut().size();
                    rp[i] = rp[i] + r[((Integer) indexMap.get(inName)).intValue()] / fanOut;
                }
                rp[i] = rp[i] + e[i];
            }
            //System.out.println("R' = ");
            MoreMath.printVector(rp);
            for (int i = 0; i < r.length; i++) {
                r[i] = rp[i];
            }
            PageRank.normalize(r);
            //System.out.println("\nNorm R = ");
            //MoreMath.printVector(r);
            //System.out.println("");
        }
        
        HashMap<String, Double> map = new HashMap<String, Double>();
        for (int i = 0; i < nodes.length; i++) {
            map.put(nodes[i].toString(), Double.valueOf(r[i]));
        }
        return map;
        
    }

    public static void countPageRanks(Graph graph, String dir) {

        HashMap<String, Double> pageRanks = countPageRank(graph, 0.15, 50);
        
        try {
            PrintWriter out = new PrintWriter(new FileWriter(new File(dir, "pageRanks.txt")));
            for (String key: pageRanks.keySet()) {
                out.println(key + " " + pageRanks.get(key));
            }
            out.close();
        }
        catch (IOException e) {
        System.err.println("HTMLPage.writeAbsolute(): " + e);
        } 
    }
}
