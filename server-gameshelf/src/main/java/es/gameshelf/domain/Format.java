package es.gameshelf.domain;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class Format extends Classification {
    /**
     * Default constructor of the class
     */
    public Format() {
    }

    /**
     * Constructor of the class
     * @param id of the format
     */
    public Format(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the format
     */
    public Format(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the format
     * @param name of the format
     */
    public Format(int id, String name) {
        super(id, name);
    }
}
