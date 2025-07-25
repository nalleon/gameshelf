package es.gameshelf.model.entities;

import es.gameshelf.domain.abstracts.Classification;
import jakarta.persistence.Entity;
import jakarta.persistence.NamedQuery;
import jakarta.persistence.Table;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name="formats")
@NamedQuery(name="FormatEntity.findAll", query="SELECT r FROM FormatEntity r")
public class FormatEntity extends Classification {
    /**
     * Default constructor of the class
     */
    public FormatEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the format
     */
    public FormatEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the format
     */
    public FormatEntity(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the format
     * @param name of the format
     */
    public FormatEntity(int id, String name) {
        super(id, name);
    }
}
