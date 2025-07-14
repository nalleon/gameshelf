package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class Developer extends Classification {
    /**
     * Default constructor of the class
     */
    public Developer() {
    }

    /**
     * Constructor of the class
     * @param id of the developer
     */
    public Developer(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the developer
     */
    public Developer(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the developer
     * @param name of the developer
     */
    public Developer(int id, String name) {
        super(id, name);
    }
}
