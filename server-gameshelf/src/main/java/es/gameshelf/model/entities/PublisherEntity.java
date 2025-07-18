package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Classification;
/**
 * @author Nabil L. A. @nalleon
 */
public class PublisherEntity extends Classification {
    /**
     * Default constructor of the class
     */
    public PublisherEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the publisher
     */
    public PublisherEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the publisher
     */
    public PublisherEntity(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the publisher
     * @param name of the publisher
     */
    public PublisherEntity(int id, String name) {
        super(id, name);
    }
}
