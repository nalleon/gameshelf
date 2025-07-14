package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class Genre extends Classification {
    /**
     * Default constructor of the class
     */
    public Genre() {
    }

    /**
     * Constructor of the class
     * @param id of the genre
     */
    public Genre(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the genre
     */
    public Genre(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the genre
     * @param name of the genre
     */
    public Genre(int id, String name) {
        super(id, name);
    }
}
