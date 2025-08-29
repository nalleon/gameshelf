package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class Tag extends Classification {
    /**
     * Default constructor of the class
     */
    public Tag() {
    }

    /**
     * Constructor of the class
     * @param id of the developer
     */
    public Tag(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the developer
     */
    public Tag(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the developer
     * @param name of the developer
     */
    public Tag(int id, String name) {
        super(id, name);
    }
}
