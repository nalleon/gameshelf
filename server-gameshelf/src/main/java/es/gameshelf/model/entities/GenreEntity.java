package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class GenreEntity extends Classification {
    /**
     * Default constructor of the class
     */
    public GenreEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the genre
     */
    public GenreEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the genre
     */
    public GenreEntity(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the genre
     * @param name of the genre
     */
    public GenreEntity(int id, String name) {
        super(id, name);
    }
}
