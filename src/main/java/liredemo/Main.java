/*
 * Main.java
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package liredemo;

import net.semanticmetadata.lire.builders.DocumentBuilder;
import net.semanticmetadata.lire.imageanalysis.features.global.ColorLayout;
import net.semanticmetadata.lire.searchers.*;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.store.FSDirectory;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
/*
 * This file is part of the Caliph and Emir project: http://www.SemanticMetadata.net.
 *
 * Caliph & Emir is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Caliph & Emir is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Caliph & Emir; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Copyright statement:
 * --------------------
 * (c) 2002-2007 by Mathias Lux (mathias@juggle.at)
 * http://www.juggle.at, http://www.SemanticMetadata.net
 */

/**
 * This file is part of the Caliph and Emir project:
 * http://www.SemanticMetadata.net
 *
 * @author You MAC
 */

public class Main {
	private static int NUM_RESULTS = 6;
	private static int SCORE_THRESH = 35;
	private IndexReader ir;
	private ImageSearcher searcher;
    private String index_path;
    public  String res;
    public  String[] res_arr;
	/**
	 * Creates a new instance of Main
	 */
	public Main() {
	    String user_dir = System.getProperty("user.dir");
	    index_path = user_dir + "/index";
	    System.out.println("user dir:" + user_dir + "; index path:" + index_path);
        System.out.println("class path:" + System.getProperty("java.class.path")); //just print classpath
		try {
			ir = DirectoryReader.open(FSDirectory.open(Paths.get(index_path)));
		} catch (IOException e) {
			e.printStackTrace();
		}
		searcher = new GenericFastImageSearcher(NUM_RESULTS, ColorLayout.class);// color layout best
        res_arr = new String[NUM_RESULTS];
	}

	public String[] searchImage(String searchImagePath) {
		res = "";
		try {
			BufferedImage img = ImageIO.read(new File(searchImagePath));
			ImageSearchHits hits = searcher.search(img, ir);

			/**
			String resultName = ir.document(hits.documentID(0)).getValues(DocumentBuilder.FIELD_NAME_IDENTIFIER)[0];
			System.out.println(resultName);
			int start = resultName.lastIndexOf("/");
			int end = resultName.lastIndexOf("_");
			if (start != -1) {
				resultName = resultName.substring(start + 1, end);
			}
			System.out.println(resultName);
             **/

			String tmp = "";
			for (int i = 0; i < NUM_RESULTS; i++) {
				tmp = ir.document(hits.documentID(i)).getValues(DocumentBuilder.FIELD_NAME_IDENTIFIER)[0];
				System.out.println(hits.score(i) + ": " + tmp);
				res = res + ";" + tmp;
				res_arr[i] = tmp;
			}

			/**
			if (hits.score(0) > SCORE_THRESH) {
				System.out.println("NULL");
				return null;
			}
             return ir.document(hits.documentID(0)).getValues(DocumentBuilder.FIELD_NAME_IDENTIFIER)[0];
             **/

			//return res;
            return res_arr;
		} catch (IOException e) {
			e.printStackTrace();
			res = "error";
			return res_arr;
		}
	}

	/**
	 * @param args
	 *            the command line arguments
	 * @throws Exception
	 */
	public static void main(String[] args) throws IOException {
		Main server = new Main();
		String searchImagePath = System.getProperty("user.dir") + "/bdimage/query/junyao.jpg";
		String[] res = server.searchImage(searchImagePath);
		System.out.println(res);
	}
}
