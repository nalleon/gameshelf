package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Tag;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface ITagRepository {
    Tag save(Tag tag);
    List<Tag> findAll();
    Tag findById(Integer id);
    Tag findByName(String name);
    boolean delete(Integer id);
    Tag update(Tag tag);
}
